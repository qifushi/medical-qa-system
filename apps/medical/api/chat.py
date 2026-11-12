import os
import sys
import base64
from PIL import Image
import io

# 添加 apps 目录到 Python 路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import requests
import re
from bs4 import BeautifulSoup
from ddgs import DDGS
from common.cmekg_client import get_cmekg_client
from .document_parser import extract_text
from django.conf import settings

# 图片上传目录
UPLOAD_DIR = os.path.join(settings.MEDIA_ROOT, 'images')

# 加载模型
model = None

def load_model():
    """加载模型"""
    global model
    try:
        print("正在加载模型...")
        # 由于 LMstudio 能够运行这个模型，我们使用 LMstudio 的 API
        print("使用 LMstudio API")
        model = "lmstudio"
        print("模型加载成功")
    except Exception as e:
        print(f"模型加载失败：{e}")
        import traceback
        traceback.print_exc()
        # 如果模型加载失败，使用一个简单的回复作为 fallback
        pass

# 存储对话历史 - 每个用户会话应该有独立的对话历史
# 由于当前是简单实现，我们使用全局变量，但在生产环境中应该使用会话管理
conversation_history = []

# 最大对话轮数
MAX_HISTORY = 2

# 重置对话历史的函数
def reset_history():
    """重置对话历史"""
    global conversation_history
    conversation_history = []

# 清理对话历史，按总字数预算截断（比按条数更稳，避免长回答撑爆上下文）
HISTORY_MAX_CHARS = 600

def clean_history():
    """清理对话历史：只保留最近 MAX_HISTORY 轮，且总字数不超过 HISTORY_MAX_CHARS"""
    global conversation_history
    if len(conversation_history) > MAX_HISTORY * 2:
        conversation_history = conversation_history[-MAX_HISTORY*2:]
    # 从最新往前累加，超出预算的旧消息丢弃
    kept, total = [], 0
    for msg in reversed(conversation_history):
        if total + len(msg) > HISTORY_MAX_CHARS:
            break
        kept.insert(0, msg)
        total += len(msg)
    conversation_history = kept

# 最近一次问答命中的知识库条目，供前端展示来源
LAST_SOURCES = []

_KB_LABELS = {
    'report_analysis': '报告分析库',
    'medicine_analysis': '药品分析库',
    'medical_service': '就医助手库',
}


def _collect_sources(local_kb_results, limit=3, min_score=0.86):
    """把检索结果整理成前端可展示的来源清单"""
    sources = []
    for block in local_kb_results or []:
        kb_name = block.get('kb_name') or ''
        for item in (block.get('results') or [])[:2]:
            meta = item.get('metadata') or {}
            name = (item.get('name') or item.get('title')
                    or meta.get('entity_name') or meta.get('name') or '')
            if not name:
                continue
            try:
                score = round(float(item.get('score') or 0), 3)
            except (TypeError, ValueError):
                score = 0.0
            # 取条目正文开头，作为"这条到底讲了什么"的说明
            props = meta.get('properties') or {}
            raw = (props.get('desc') or props.get('indications') or props.get('适应症')
                   or props.get('question') or meta.get('desc') or meta.get('answer')
                   or meta.get('question') or item.get('answer') or item.get('content')
                   or item.get('desc') or '')
            snippet = re.sub(r'<[^>]+>', '', str(raw))
            snippet = ' '.join(snippet.split())[:40]
            sources.append({
                'name': str(name),
                'kb': _KB_LABELS.get(kb_name, kb_name),
                'score': score,
                'snippet': snippet,
            })
    sources.sort(key=lambda x: -x['score'])
    # 只展示高置信条目，避免把检索噪声当成"来源"暴露给用户
    return [s for s in sources if s['score'] >= min_score][:limit]


def get_last_sources():
    return list(LAST_SOURCES)

def image_to_base64(image_path, optimize=True, max_size=600, quality=60):
    """将图片转换为Base64格式，可选择优化"""
    try:
        if optimize:
            # 优化图片
            img = Image.open(image_path)
            # 转换为 RGB 模式，确保支持 JPEG 格式
            if img.mode == 'RGBA':
                img = img.convert('RGB')
            # 调整图片大小
            if max(img.size) > max_size:
                img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
            
            # 保存为 JPEG 格式
            buffer = io.BytesIO()
            img.save(buffer, format="JPEG", quality=quality, optimize=True)
            buffer.seek(0)
            image_data = buffer.read()
            # 强制使用 JPEG 格式
            ext = 'jpeg'
        else:
            with open(image_path, "rb") as f:
                image_data = f.read()
            # 获取图片格式
            ext = os.path.splitext(image_path)[1].lower().replace('.', '')
            if ext == 'jpg':
                ext = 'jpeg'
        
        encoded = base64.b64encode(image_data).decode('utf-8')
        
        return f"data:image/{ext};base64,{encoded}"
    except Exception as e:
        print(f"图片转换失败：{e}")
        return None

def search_web(query):
    """搜索线上网站，获取相关网页内容"""
    try:
        # 使用 DuckDuckGo 搜索（完全免费，无需 API 密钥）
        webpages = []
        web_urls = []
        
        print(f"开始搜索：{query}")
        
        # 伪装成真实浏览器的 headers
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        
        # 重试机制
        from requests.adapters import HTTPAdapter
        from urllib3.util.retry import Retry
        
        session = requests.Session()
        retries = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
        session.mount('http://', HTTPAdapter(max_retries=retries))
        session.mount('https://', HTTPAdapter(max_retries=retries))
        
        # 医疗相关的域名白名单
        medical_domains = [
            'dxy.com', 'haodf.com', '39.net', '120ask.com', 'medicalnewstoday.com',
            'mayoclinic.org', 'webmd.com', 'nhs.uk', 'who.int', 'cdc.gov',
            'zhihu.com', 'baidu.com', 'sogou.com', 'bing.com', 'google.com'
        ]
        
        # 过滤不适合的内容关键词
        inappropriate_keywords = [
            'porn', 'sex', 'adult', 'xxx', 'pregnancy', 'pregnant', '孕妇',
            'bombing', '黑料', '不打烊', '私处', '外阴', '阴道', '妇科',
            '月经', '避孕', '流产', '宫外孕', '宫颈', '卵巢', '子宫'
        ]
        
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=5))
                print(f"搜索结果数量：{len(results)}")
                
                for r in results:
                    url = r.get('href')
                    title = r.get('title')
                    snippet = r.get('body')
                    
                    # 过滤不适合的内容
                    if any(keyword in url.lower() or keyword in title.lower() or keyword in (snippet or '') for keyword in inappropriate_keywords):
                        print(f"跳过不适合的结果：{title} - {url}")
                        continue
                    
                    # 优先选择医疗相关域名
                    domain = url.split('/')[2] if len(url.split('/')) > 2 else ''
                    if not any(medical_domain in domain for medical_domain in medical_domains):
                        print(f"跳过非医疗域名：{title} - {url}")
                        continue
                    
                    print(f"处理结果：{title} - {url}")
                    
                    # 尝试获取网页内容
                    try:
                        page_response = session.get(url, headers=headers, timeout=10)
                        page_response.raise_for_status()
                        soup = BeautifulSoup(page_response.content, "html.parser")
                        
                        # 提取网页标题
                        page_title = soup.title.string if soup.title else title
                        
                        # 提取网页正文内容
                        paragraphs = soup.find_all(["p", "h1", "h2", "h3", "h4", "h5", "h6"])
                        content = " ".join([p.get_text(strip=True) for p in paragraphs])
                        
                        # 限制内容长度
                        content = content[:2000]
                        
                        webpages.append({
                            "url": url,
                            "name": title,
                            "title": page_title,
                            "snippet": snippet,
                            "content": content
                        })
                    except Exception as e:
                        print(f"获取网页内容失败：{e}")
                        # 如果获取网页内容失败，仍然添加结果，只使用搜索结果中的信息
                        webpages.append({
                            "url": url,
                            "name": title,
                            "title": title,
                            "snippet": snippet,
                            "content": snippet
                        })
                        
                    # 只返回前 3 个结果
                    if len(webpages) >= 3:
                        break
        except Exception as e:
            print(f"DDGS 搜索失败：{e}")
            # 如果 DDGS 搜索失败，使用备用搜索方法
            # 这里可以添加其他搜索 API 或使用固定的医疗信息
            # 暂时返回空列表
            pass
        
        print(f"搜索完成，返回 {len(webpages)} 个结果")
        return webpages
    except Exception as e:
        print(f"搜索失败：{e}")
        # 如果搜索失败，返回空列表
        return []

def medical_chat(content, smart_search=False, deep_think=False, kb_type=None):
    """医疗助手对话函数
    
    Args:
        content: 用户输入内容
        smart_search: 是否启动智能搜索（联网搜索）
        deep_think: 是否启动深度思考（生成思考过程）
        kb_type: 知识库类型（report_analysis, medical_service, medicine_analysis）
    """
    global conversation_history
    
    # 如果模型未加载，使用 fallback 回复
    if model is None:
        return "您好，我是知贝医疗助手。由于模型正在加载中，暂时无法提供详细医疗咨询。请稍后再试，或咨询专业医生获取准确的医疗建议。"
    
    try:
        # 清理用户输入，确保不包含特殊字符
        clean_content = content.strip()
        
        # 构建对话历史字符串（不包含当前问题）
        history_str = "\n\n".join(conversation_history)
        
        # 根据 smart_search 参数决定是否搜索网页
        webpages = []
        if smart_search:
            print("启动智能搜索，开始搜索线上网站...")
            webpages = search_web(clean_content)
        else:
            print("未启动智能搜索，跳过联网搜索")
        
        # 构建网页信息字符串
        web_info = ""
        web_urls = []
        if webpages:
            web_info = "以下是相关网页信息：\n"
            for i, page in enumerate(webpages):
                web_info += f"\n{i+1}. {page['title']}\n"
                web_info += f"   摘要：{page['snippet']}\n"
                web_info += f"   内容：{page['content']}\n"
                web_urls.append(page['url'])
        
        # 获取本地知识库知识
        cmekg = get_cmekg_client()
        if kb_type:
            print(f"使用指定知识库：{kb_type}")
            knowledge = cmekg.query(clean_content, kb_type=kb_type)
        else:
            print("不使用指定知识库，查询所有本地知识库")
            # 一次查询三个知识库并合并结果
            kb_names = ['report_analysis', 'medicine_analysis', 'medical_service']
            combined_summary = ""
            combined_entities = []
            combined_relations = []
            combined_local_kb_results = []
            
            for kb_name in kb_names:
                try:
                    kb_result = cmekg.query(clean_content, kb_type=kb_name)
                    if kb_result.get('summary'):
                        kb_label = {
                            'report_analysis': '报告分析',
                            'medicine_analysis': '药品分析',
                            'medical_service': '就医助手'
                        }.get(kb_name, kb_name)
                        combined_summary += f"\n【{kb_label}知识库】:\n{kb_result['summary']}\n"
                    if kb_result.get('entities'):
                        combined_entities.extend(kb_result['entities'])
                    if kb_result.get('relations'):
                        combined_relations.extend(kb_result['relations'])
                    if kb_result.get('local_kb_results'):
                        combined_local_kb_results.extend(kb_result['local_kb_results'])
                except Exception as e:
                    print(f"查询知识库 {kb_name} 失败：{e}")
            
            knowledge = {
                "summary": combined_summary,
                "entities": combined_entities,
                "relations": combined_relations,
                "local_kb_results": combined_local_kb_results
            }
            print(f"已合并三个知识库的查询结果")
        
        # 记录命中的知识库条目，供前端展示来源
        global LAST_SOURCES
        LAST_SOURCES = _collect_sources(knowledge.get('local_kb_results') or [])

        # 把知识加到 prompt 里
        if knowledge['summary']:
            if web_info:
                web_info += f"\n本地知识库知识：\n{knowledge['summary']}\n"
            else:
                web_info = f"本地知识库知识：\n{knowledge['summary']}\n"
        
        # 构建医疗助手的 prompt
        # 根据 deep_think 参数决定是否要求生成思考过程
        if deep_think:
            print("启动深度思考，将生成思考过程")
            think_instruction = """重要要求：
1. 首先生成内部思考过程，使用<think>标签包裹，格式为：<think>思考过程内容</think>思考过程是你的内部推理，应该：
   - 分析用户当前提供的信息（只分析已有信息，不假设）
   - 分析相关网页信息和本地知识库，提取有用的医疗建议
   - 分析对话历史，理解上下文语境，特别注意用户问题中的指代关系（如"这个"、"那"等代词）
   - 分析上传的图片内容，提取相关的医疗信息
   - 指出信息是否完整，缺少哪些关键信息
   - 规划如何回答（先给通用建议，再引导补充信息）
   - 思考过程中不要直接向用户提问，提问应该在正式回复中
    
2. 然后生成正式回复，不要包含思考过程
   - 正式回复是给用户看的内容
   - 基于用户问题、对话历史、相关网页信息和图片内容，提供专业、准确的医疗建议
   - 特别注意理解用户问题中的指代关系，结合对话历史进行分析
   - 如果信息不足，在正式回复中引导用户补充信息
   - 所有提问、建议都在正式回复中

3. 所有内容必须使用中文

4. 思考过程要详细，分析用户问题和上下文
4.1 只基于用户已提供的信息进行分析，不要假设或补充用户未提及的症状、时间、年龄等细节
4.2 当用户未提供具体数值、症状等信息时，严禁在思考过程或回复中自行添加任何具体数值（如血压值、心率）、具体症状（如头晕、头痛）或其他未提及的细节。
4.3 如果用户信息不足，正确的做法是：
   - 在思考过程中指出信息不足，需要用户补充
   - 在正式回复中说明目前信息有限，只能提供通用建议
   - 在正式回复中列出需要用户补充的关键信息（如具体数值、症状、年龄等），让用户自行提供
5. 正式回复必须使用清晰的层级结构，同类建议必须合并，严禁重复
6. 正式回复的格式要求：
   - 使用一、二、三或 1. 2. 3. 等层级标题
   - 将相关建议归类合并，不要分散重复
   - 按重要性或操作顺序排列
   - 就医指征单独放在最后
7. 严格基于用户实际提供的信息、对话历史和相关网页信息，不要引入用户未提及的信息
8. 不要假设用户的年龄、性别、体温等任何未明确提供的个人信息
9. 基于对话历史提供连续的、上下文相关的回复
10. 只针对用户当前的问题进行回复，不要生成额外的假设问题或回复
11. 不要在回复中包含'用户:'或'助手:'这样的标签
12. 特别注意：如果用户只提到了'瘙痒'等症状，没有提到具体部位，不要假设是女性隐私部位的问题，应该提供通用的瘙痒处理建议
13. 正式回复要展开写，不受字数限制。必须按下面 7 个小节逐项写，不得省略、不得合并：
    ① 结论（只写一句话，直接回答问题，不要重复、不要写"即："）
    ② 作用与原理
    ③ 用法用量（成人、儿童分开写）
    ④ 注意事项与禁忌
    ⑤ 不良反应与配伍禁忌
    ⑥ 与其他剂型、同类药的区别
    ⑦ 就医指征
    即使某个小节信息少，也要写出来并说明说明书是否明确，不允许跳过；7 个小节合计不少于 500 字
14. 知识库没有的内容，直接用通用医学知识补充，不需要逐句标注；只有当通用知识与知识库说法冲突时，才说明差异并以知识库为准
15. 第 4.2、7、8 条限制的是不要虚构患者个人信息，并不限制补充通用医学知识
16. 涉及药品时尽量写清：适应证、成人用法用量、儿童用法用量、禁忌、不良反应、配伍禁忌
17. 只使用和当前问题直接相关的知识库条目。知识库里出现但与问题无关的疾病、症状、药物内容，一律不要写进回答
18. 严禁重复：同一句话、同一条注意事项在回答里只能出现一次，不要换个说法再写一遍
19. 药品名称、别名、成分、剂型一律以知识库为准：知识库给出别名（例如"腺嘌呤"）时必须照用，严禁自行补充、替换或改写别称与化学成分
"""
        else:
            print("未启动深度思考，不生成思考过程")
            think_instruction = """重要要求：
1. 直接生成正式回复，不需要思考过程
2. 基于用户问题、对话历史、相关网页信息和图片内容，提供专业、准确的医疗建议
3. 特别注意理解用户问题中的指代关系，结合对话历史进行分析
4. 分析上传的图片内容，提取相关的医疗信息
5. 如果信息不足，在回复中引导用户补充信息
6. 所有内容必须使用中文
7. 正式回复必须使用清晰的层级结构，同类建议必须合并，严禁重复
8. 正式回复的格式要求：
   - 使用一、二、三或 1. 2. 3. 等层级标题
   - 将相关建议归类合并，不要分散重复
   - 按重要性或操作顺序排列
   - 就医指征单独放在最后
9. 严格基于用户实际提供的信息、对话历史和相关网页信息，不要引入用户未提及的信息
10. 不要假设用户的年龄、性别、体温等任何未明确提供的个人信息
11. 基于对话历史提供连续的、上下文相关的回复
12. 只针对用户当前的问题进行回复，不要生成额外的假设问题或回复
13. 不要在回复中包含'用户:'或'助手:'这样的标签
14. 特别注意：如果用户只提到了'瘙痒'等症状，没有提到具体部位，不要假设是女性隐私部位的问题，应该提供通用的瘙痒处理建议
15. 回答要展开写，不要一句话结论。必须按下面 7 个小节逐项写，不得省略、不得合并：
    ① 结论（只写一句话，直接回答问题，不要重复、不要写"即："）
    ② 作用与原理
    ③ 用法用量（成人、儿童分开写）
    ④ 注意事项与禁忌
    ⑤ 不良反应与配伍禁忌
    ⑥ 与其他剂型、同类药的区别
    ⑦ 就医指征
    即使某个小节信息少，也要写出来并说明说明书是否明确，不允许跳过；7 个小节合计不少于 500 字
16. 知识库没有的内容，直接用通用医学知识补充，不需要逐句标注；只有当通用知识与知识库说法冲突时，才说明差异并以知识库为准
17. 第 9、10 条限制的是不要虚构患者个人信息（年龄、性别、数值、症状），并不限制补充通用医学知识
18. 涉及药品时尽量写清：适应证、成人用法用量、儿童用法用量、禁忌、不良反应、配伍禁忌
19. 只使用和当前问题直接相关的知识库条目。知识库里出现但与问题无关的疾病、症状、药物内容，一律不要写进回答
20. 严禁重复：同一句话、同一条注意事项在回答里只能出现一次，不要换个说法再写一遍
21. 药品名称、别名、成分、剂型一律以知识库为准：知识库给出别名（例如"腺嘌呤"）时必须照用，严禁自行补充、替换或改写别称与化学成分
"""
        
        prompt = f"""你是知贝医疗助手，一个专业的医疗 AI 助手。请根据用户的问题、对话历史、相关网页信息和上传的图片内容提供专业、准确的医疗建议。

{web_info}

{think_instruction}

对话历史：
{history_str}

用户当前问题：
{clean_content}

输出格式硬要求（优先级最高）：
必须按 ① 结论 ② 作用与原理 ③ 用法用量 ④ 注意事项与禁忌 ⑤ 不良反应与配伍禁忌 ⑥ 与其他剂型、同类药的区别 ⑦ 就医指征 输出 7 个小节，每节单独成段，合计不少于 500 字。
药品名称、别名、成分、剂型只允许写上文知识库中出现的内容，不得自行补充或改写。

助手："""
        
        # 更新对话历史（在构建 prompt 之后，确保当前问题也被记录）
        conversation_history.append(f"用户：{clean_content}")
        
        # 清理对话历史，只保留最近的 MAX_HISTORY 轮对话
        clean_history()
        
        # 使用 LMstudio / Ollama 兼容 API 生成回复（地址可通过环境变量覆盖）
        url = os.getenv("LMSTUDIO_API_URL", "http://localhost:1234/v1/chat/completions")
        headers = {
            "Content-Type": "application/json"
        }
        # 构建消息内容，支持图片分析
        messages = [
            {
                "role": "system",
                "content": "你是知贝医疗助手，一个专业的医疗 AI 助手。"
            }
        ]
        
        # 检查是否有图片上传
        import re
        # 更灵活的正则表达式，匹配各种格式的图片URL
        image_urls = re.findall(r'图片:.*?\(([^)]+)\)', clean_content)
        # 检查是否有文件上传
        file_urls = re.findall(r'文件:.*?\(([^)]+)\)', clean_content)
        
        if image_urls or file_urls:
            # 提取用户的文字描述（去掉文件信息）
            user_description = re.sub(r'上传的文件：.*', '', clean_content, flags=re.DOTALL)
            user_description = user_description.strip()
            
            # 构建包含图片或文件的消息
            content_parts = [
                {
                    "type": "text",
                    "text": user_description
                }
            ]
            
            # 处理每张图片
            for image_url in image_urls:
                # 从URL中提取图片文件名
                image_filename = os.path.basename(image_url)
                # 构建完整的图片路径
                image_path = os.path.join(UPLOAD_DIR, image_filename)
                
                # 检查图片文件是否存在
                if os.path.exists(image_path):
                    # 转换图片为Base64，带优化
                    base64_image = image_to_base64(image_path, optimize=True, max_size=600, quality=60)
                    if base64_image:
                        content_parts.append({
                            "type": "image_url",
                            "image_url": {
                                "url": base64_image
                            }
                        })
                    else:
                        # 如果图片转换失败，使用原始URL
                        content_parts.append({
                            "type": "text",
                            "text": f"图片URL: {image_url}"
                        })
                else:
                    # 如果图片文件不存在，尝试查找其他可能的路径
                    # 检查是否存在类似的文件（可能是文件名大小写问题）
                    found = False
                    for filename in os.listdir(UPLOAD_DIR):
                        if filename.lower() == image_filename.lower():
                            # 找到匹配的文件
                            image_path = os.path.join(UPLOAD_DIR, filename)
                            base64_image = image_to_base64(image_path, optimize=True, max_size=600, quality=60)
                            if base64_image:
                                content_parts.append({
                                    "type": "image_url",
                                    "image_url": {
                                        "url": base64_image
                                    }
                                })
                                found = True
                                break
                    
                    if not found:
                        # 如果仍然找不到文件，使用原始URL
                        print(f"图片文件不存在：{image_path}")
                        content_parts.append({
                            "type": "text",
                            "text": f"图片URL: {image_url}"
                        })
            
            # 处理每个文件
            for file_url in file_urls:
                # 从URL中提取文件名
                file_filename = os.path.basename(file_url)
                # 构建完整的文件路径
                file_path = os.path.join(settings.MEDIA_ROOT, 'files', file_filename)

                resolved_path = None
                if os.path.exists(file_path):
                    resolved_path = file_path
                else:
                    # 文件名大小写不一致时，在目录中做一次忽略大小写匹配
                    files_dir = os.path.join(settings.MEDIA_ROOT, 'files')
                    if os.path.isdir(files_dir):
                        for filename in os.listdir(files_dir):
                            if filename.lower() == file_filename.lower():
                                resolved_path = os.path.join(files_dir, filename)
                                file_filename = filename
                                break

                if resolved_path:
                    try:
                        # 按文件类型解析：PDF / docx / 纯文本
                        file_content = extract_text(resolved_path)
                        if file_content:
                            content_parts.append({
                                "type": "text",
                                "text": f"\n【文件内容 - {file_filename}】:\n{file_content}"
                            })
                        else:
                            content_parts.append({
                                "type": "text",
                                "text": f"\n【文件 - {file_filename}】未提取到文本，可能是扫描件或空文件。"
                                        f"请改用图片上传，或直接输入报告中的文字内容。"
                            })
                    except Exception as e:
                        print(f"读取文件失败：{e}")
                        content_parts.append({
                            "type": "text",
                            "text": f"\n【文件 - {file_filename}】无法解析：{e}"
                        })
                else:
                    print(f"文件不存在：{file_path}")
                    content_parts.append({
                        "type": "text",
                        "text": f"文件URL: {file_url}"
                    })
            
            messages.append({
                "role": "user",
                "content": content_parts
            })
        else:
            # 普通文本消息
            messages.append({
                "role": "user",
                "content": prompt
            })
        
        # 使用用户指定的模型
        data = {
            "model": os.getenv("LMSTUDIO_MODEL", "qwen3-vl-4b-instruct"),
            "messages": messages,
            "max_tokens": 2048,
            "temperature": 0.7
        }
        
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        
        # 提取助手的回复部分
        response_json = response.json()
        assistant_response = response_json["choices"][0]["message"]["content"]
        
        # 提取思考过程和实际回复
        think_part = ""
        actual_response = ""
        
        # 首先检查是否有"思考过程"标记
        if "思考过程" in assistant_response:
            # 找到思考过程的开始位置
            think_start = assistant_response.find("思考过程")
            # 找到思考过程的结束位置
            # 尝试找到"正式回复："标记
            formal_start = assistant_response.find("正式回复：", think_start)
            if formal_start != -1:
                # 提取思考过程
                think_part = assistant_response[think_start:formal_start].strip()
                # 提取实际回复
                actual_response = assistant_response[formal_start + len("正式回复："):].strip()
            else:
                # 尝试找到"一、"、"1."等正式回复的开始标记
                # 这些标记通常表示正式回复的开始
                formal_start = -1
                # 查找常见的标题标记
                patterns = ["一、", "1.", "1、", "首先", "第一"]
                for pattern in patterns:
                    pos = assistant_response.find(pattern, think_start)
                    if pos != -1:
                        formal_start = pos
                        break
                
                if formal_start != -1:
                    # 提取思考过程
                    think_part = assistant_response[think_start:formal_start].strip()
                    # 提取实际回复
                    actual_response = assistant_response[formal_start:].strip()
                else:
                    # 如果没有找到正式回复的开始标记，尝试其他方式
                    think_end = assistant_response.find("▶", think_start)
                    if think_end == -1:
                        think_end = len(assistant_response)
                    # 提取思考过程
                    think_part = assistant_response[think_start:think_end].strip()
                    # 尝试从思考过程中提取实际回复
                    # 查找思考过程中的引导信息部分
                    guide_start = think_part.find("需引导用户提供以下信息")
                    if guide_start != -1:
                        # 如果找到引导信息，将引导信息作为实际回复的一部分
                        actual_response = think_part[guide_start:].strip()
                        # 保留引导信息之前的内容作为思考过程
                        think_part = think_part[:guide_start].strip()
                    else:
                        # 如果没有找到引导信息，尝试从整个回复中提取
                        # 查找"参考网页地址"标记
                        web_start = assistant_response.find("参考网页地址", think_end)
                        if web_start != -1:
                            # 实际回复是思考过程之后、参考网页地址之前的内容
                            actual_response = assistant_response[think_end:web_start].strip()
                        else:
                            # 实际回复是思考过程之后的所有内容
                            actual_response = assistant_response[think_end:].strip()
        elif "<think>" in assistant_response and "</think>" in assistant_response:
            # 提取思考过程
            think_start = assistant_response.find("<think>")
            think_end = assistant_response.find("</think>")
            think_part = assistant_response[think_start + 6:think_end].strip()
            
            # 提取实际回复（去除思考过程部分）
            actual_response = assistant_response[:think_start].strip() + assistant_response[think_end + 8:].strip()
        elif "思考过程内容：" in assistant_response:
            # 处理模型生成的另一种格式
            think_start = assistant_response.find("思考过程内容：") + len("思考过程内容：")
            # 找到思考过程的结束位置（通常是在"▶"或"参考网页地址"之前）
            think_end = assistant_response.find("▶", think_start)
            if think_end == -1:
                think_end = assistant_response.find("参考网页地址", think_start)
            if think_end == -1:
                think_end = len(assistant_response)
            think_part = assistant_response[think_start:think_end].strip()
            
            # 提取实际回复（去除思考过程部分）
            actual_response = assistant_response[:think_start - len("思考过程内容：")].strip()
            # 检查是否有"▶"标记，如果有，保留其之前的内容
            arrow_pos = actual_response.find("▶")
            if arrow_pos != -1:
                actual_response = actual_response[:arrow_pos].strip()
        elif "</think>" in assistant_response:
            # 处理格式错误的情况，假设思考过程在开头
            think_end = assistant_response.find("</think>")
            think_part = assistant_response[:think_end].strip()
            actual_response = assistant_response[think_end + 8:].strip()
        else:
            # 没有思考过程，直接使用整个回复
            actual_response = assistant_response
            # 检查是否有"▶"标记，如果有，保留其之前的内容
            arrow_pos = actual_response.find("▶")
            if arrow_pos != -1:
                actual_response = actual_response[:arrow_pos].strip()
        
        # 如果实际回复为空，尝试从思考过程中提取
        if not actual_response:
            # 检查思考过程中是否包含"正式回复："标记
            formal_start = think_part.find("正式回复：")
            if formal_start != -1:
                actual_response = think_part[formal_start + len("正式回复："):].strip()
                think_part = think_part[:formal_start].strip()
        
        # 处理实际回复，过滤掉模型生成的幻觉内容
        import re
        # 过滤掉"用户:"、"助手:"等标签
        actual_response = re.sub(r'用户:.*?[\n\r]', '', actual_response)
        actual_response = re.sub(r'助手:.*?[\n\r]', '', actual_response)
        # 过滤掉"当前问题："等幻觉内容
        actual_response = re.sub(r'当前问题：.*?[\n\r]', '', actual_response)
        # 过滤掉多余的空行
        actual_response = re.sub(r'\n{3,}', '\n\n', actual_response)
        # 过滤掉"请根据上述要求，输出正式回复内容"等幻觉内容
        actual_response = re.sub(r'请根据上述要求，输出正式回复内容.*?[\n\r]', '', actual_response)
        
        # 如果实际回复为空，使用默认消息
        if not actual_response:
            actual_response = "您好，我是知贝医疗助手。根据您的描述，我需要更多信息来为您提供准确的医疗建议。"
        
        # 处理 Markdown 格式
        # 将 ** 替换为 <strong> 标签
        actual_response = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', actual_response)
        # 将 ### 标题替换为 <h3> 标签
        actual_response = re.sub(r'^### (.+)$', r'<h3>\1</h3>', actual_response, flags=re.MULTILINE)
        # 将 ## 标题替换为 <h2> 标签
        actual_response = re.sub(r'^## (.+)$', r'<h2>\1</h2>', actual_response, flags=re.MULTILINE)
        # 将 # 标题替换为 <h1> 标签
        actual_response = re.sub(r'^# (.+)$', r'<h1>\1</h1>', actual_response, flags=re.MULTILINE)
        # 将 --- 分隔线替换为 <hr> 标签
        actual_response = re.sub(r'^\s*---\s*$', r'<hr>', actual_response, flags=re.MULTILINE)
        # 将 - 列表替换为 <li> 标签
        actual_response = re.sub(r'^\s*\- (.+)$', r'<li>\1</li>', actual_response, flags=re.MULTILINE)
        # 处理连续的列表项，添加 <ul> 标签
        actual_response = re.sub(r'(<li>.*?</li>)', r'<ul>\1</ul>', actual_response, flags=re.DOTALL)
        # 将换行符替换为 HTML 的<br>标签，确保前端正确显示分行
        actual_response = actual_response.replace('\n', '<br>')
        
        # 处理思考过程
        if think_part:
            # 过滤掉思考过程中的幻觉内容
            think_part = re.sub(r'用户:.*?[\n\r]', '', think_part)
            think_part = re.sub(r'助手:.*?[\n\r]', '', think_part)
            # 将 Markdown 格式的**替换为 HTML 的<strong>标签
            think_part = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', think_part)
            # 将思考过程中的换行符替换为 HTML 的<br>标签
            think_part = think_part.replace('\n', '<br>')
        
        # 构建网页地址折叠栏
        web_urls_str = ""
        if smart_search:
            web_urls_str = "<urls>"
            if web_urls:
                for i, url in enumerate(web_urls):
                    web_urls_str += f"{i+1}. {url}<br>"
            else:
                web_urls_str += "未找到相关网页信息"
            web_urls_str += "</urls>"
        
        # 构建完整回复，包含实际回复、网页地址和思考过程
        # 注意：网页地址应该放在思考过程前面
        if think_part:
            full_response = f"{actual_response}{web_urls_str}<think>{think_part}</think>"
        elif deep_think:
            # 如果深度思考已启动但模型没有生成思考过程，生成一个默认的思考过程
            default_think = "我已启动深度思考模式，分析了用户的问题和相关信息，为用户提供了专业的医疗建议。"
            full_response = f"{actual_response}{web_urls_str}<think>{default_think}</think>"
        else:
            full_response = f"{actual_response}{web_urls_str}"
        
        # 更新对话历史，只存储纯文本（去掉 HTML 标签）
        import re
        pure_response = re.sub(r'<[^>]+>', '', actual_response)  # 去掉所有 HTML 标签
        pure_response = pure_response.replace('<br>', ' ')       # 把换行替换为空格
        conversation_history.append(f"助手：{pure_response[:150]}")
        
        # 清理对话历史，只保留最近的 MAX_HISTORY 轮对话
        clean_history()

        # 把命中的知识库条目直接拼进正文，确保任何前端版本都能看到
        if LAST_SOURCES:
            chips = ''.join(
                f'<div style="margin-top:8px;padding:8px 12px;border-radius:8px;'
                f'background:#f2f9f8;border-left:3px solid #0a9c88;">'
                f'<strong style="color:#0a7c6e;font-size:13px;">{s["name"]}</strong>'
                f'<span style="color:#8a9399;font-size:11px;">（{s["kb"]}）</span>'
                + (f'<div style="color:#5f6b6e;font-size:12px;margin-top:3px;line-height:1.5;">{s["snippet"]}</div>' if s.get('snippet') else '')
                + '</div>'
                for s in LAST_SOURCES
            )
            full_response += (
                '<div style="margin-top:16px;padding-top:10px;border-top:1px dashed #dbe4e6;">'
                '<div style="font-size:12px;color:#8a9399;margin-bottom:2px;">📚 参考知识库条目</div>'
                + chips + '</div>'
            )

        return full_response

    except Exception as e:
        print(f"对话生成失败：{e}")
        import traceback
        traceback.print_exc()
        # 如果 LMstudio API 调用失败，返回错误信息
        return f"抱歉，暂时无法连接到模型服务。错误信息：{str(e)}"

# 初始化加载模型
load_model()
