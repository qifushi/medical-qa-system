# 知贝医疗（medical 独立项目）

基于本地大模型与私有医疗知识库的问答系统。后端 Django + 前端 Vue3，自带三通道混合检索算法（TF-IDF + LSA + 实体覆盖），全链路本地运行，不依赖任何云服务。

## 系统组成

- **后端**：Django（`medical_project.settings`），SQLite，端口 `8010`
- **前端**：Vue3 + Vite（`ui/`），开发服务器端口 `5173`
- **大模型**：本地 OpenAI 兼容接口（默认 `http://127.0.0.1:11434/v1`），模型在 `.env` 中配置，推荐 `qwen2.5vl:7b`（支持图片输入）
- **知识库**：三个库，共约 25 万条实体
  - 报告分析（report_analysis）：102,680 条
  - 药品分析（medicine_analysis）：82,641 条
  - 就医助手（medical_service）：64,569 条

> 知识库数据与索引缓存体积过大，未纳入本仓库，准备方法见下文「知识库准备」。

## 核心算法：三通道加权融合检索

代码位于 `apps/common/knowledge/hybrid_retriever.py`：

1. **词法通道（权重 0.60）**：jieba 搜索模式分词 + 停用词过滤 + 1~2 gram，TF-IDF（sublinear，词表上限 50000）余弦相似度
2. **语义通道（权重 0.10）**：TF-IDF → TruncatedSVD 96 维 LSA 稠密向量余弦相似度，召回同义改写问法
3. **实体覆盖通道（权重 0.30）**：查询词与实体名称/科室/检查/用药/治疗标签的覆盖率重排，实体名命中额外加 0.10 奖励

融合流程：词法 Top60 ∪ 语义 Top60 作为候选池 → 各通道分数 min-max 归一化 → 加权求和 → Top5 注入大模型 prompt（RAG）。

实验脚本在 `scripts/`：`build_eval_dataset.py`（构建评估集）、`eval_retrieval.py`（计算 Recall@1/5/10、MRR、nDCG）、`tune_weights.py`（权重调优）。

## 目录结构

```
medical/
├── manage.py                      # Django 入口
├── start_medical.ps1              # 后端启动脚本
├── .env.example                   # 配置模板（复制为 .env）
├── requirements-medical.txt       # Python 依赖
├── medical_project/               # Django 配置（settings / urls）
├── apps/
│   ├── medical/
│   │   ├── api/chat.py            # 问答入口：检索 + prompt 组装 + 调用大模型
│   │   ├── api/document_parser.py # PDF / 图片解析（fitz + PaddleOCR）
│   │   └── views/                 # 对话、上传接口
│   └── common/
│       ├── cmekg_client.py        # CMeKG 医学 NLP + 知识库查询
│       └── knowledge/
│           ├── hybrid_retriever.py  # ★ 三通道混合检索算法
│           ├── knowledge_base.py    # 知识库数据层
│           └── ...
├── data/                          # 数据目录（本仓库未包含）
│   ├── knowledge_bases/           # 三个知识库的 entities.json
│   └── index_cache/               # 检索索引缓存 hybrid_v4_*.pkl
├── tools/CMeKG_tools-main/        # CMeKG 预训练模型（本仓库未包含）
├── scripts/                       # 建索引、评估、调参脚本
└── ui/                            # Vue3 前端
    └── public/medical/img/        # 前端图片（由 Django /medical/ 映射）
```

## 环境要求

- Python 3.11+
- Node.js 18+
- 本地大模型服务（Ollama / LM Studio 均可，需提供 OpenAI 兼容接口）

## 快速开始

### 1. 安装依赖

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements-medical.txt

cd ui
npm install
cd ..
```

### 2. 配置

```powershell
Copy-Item .env.example .env
```

按需修改 `.env` 中的 `LMSTUDIO_API_URL` 与 `LMSTUDIO_MODEL`。

### 3. 准备知识库（见下一节）

### 4. 启动后端（窗口 1）

```powershell
.\start_medical.ps1
```

或手动：

```powershell
.\.venv\Scripts\activate
$env:PYTHONPATH = "$PWD\apps"
python manage.py runserver 127.0.0.1:8010
```

启动成功标志：日志出现 `CMeKG 模型加载成功` 与 `Starting development server at http://127.0.0.1:8010/`。

### 5. 启动前端（窗口 2）

```powershell
cd ui
npm run dev
```

## 知识库准备

本仓库只含代码，不含知识库数据（约 774 MB）、索引缓存（约 395 MB）和 CMeKG 模型权重（约 3 GB）。缺少这些时**代码可启动，但检索为空、回答退化为纯模型生成**。

### 第一步：获取知识库数据

从 Release 下载数据包（87 MB，解压后约 350 MB）：

**[medical_knowledge_bases.zip](https://github.com/qifushi/medical-qa-system/releases/download/v1.0-kb-data/medical_knowledge_bases.zip)**

解压到项目根目录，得到：

```
data/
└── knowledge_bases/
    ├── report_analysis/entities.json      约 10 万条（问答型）
    ├── medicine_analysis/entities.json    约 8 万条（药品型）
    └── medical_service/entities.json      约 6 万条（问答型）
```

> 单个 `entities.json` 均超过 100 MB，超出 GitHub 仓库单文件上限，因此通过 Release 附件分发，不随代码克隆。

`entities.json` 为 UTF-8 编码的 JSON 数组（注意：文件若带 BOM，请用 `utf-8-sig` 读取）。每一项支持两种结构，代码会自动兼容：

```jsonc
// 结构一：扁平问答型
{
  "type": "entity",
  "entity_type": "disease",
  "entity_name": "xxx 是什么病？",
  "question": "...",
  "answer": "...",
  "department": "消化科"
}

// 结构二：嵌套属性型（疾病百科 / 药品）
{
  "type": "entity",
  "entity_type": "drug",
  "entity_name": "维生素B4",
  "properties": {
    "alias": "维生素B4；6-氨基嘌呤；腺嘌呤",
    "indications": "用于各种原因引起的白细胞减少症…",
    "usage": "1.口服给药：成人每次10～20mg，每天3次…",
    "precautions": "…",
    "interactions": "…"
  }
}
```

`properties` 下的字段会被展开参与提示词组装，常用的有 `desc`、`indications`、`usage`、`precautions`、`contraindications`、`adverse_reactions`、`interactions`、`alias`、`check`、`symptom`、`cure_way`。

**没有现成数据时**，放一个含 10~20 条记录的 `entities.json` 就能跑通全链路，用于验证环境。

### 第二步：放置 CMeKG 模型（可选）

CMeKG（Chinese Medical Knowledge Graph）是中文医学知识图谱工具集，提供医学分词、实体识别、关系抽取三个 BERT 模型，合计约 3 GB，不随本仓库分发。

**代码仓库**：https://github.com/king-yyf/CMeKG_tools
**项目主页**：https://cmekg.pcl.ac.cn/

**模型下载**（百度网盘，作者提供的原始链接）：

| 模型 | 链接 | 密码 |
|---|---|---|
| 关系抽取 RE | https://pan.baidu.com/s/1cIse6JO2H78heXu7DNewmg | `4s6k` |
| 实体识别 NER | https://pan.baidu.com/s/16TPSMtHean3u9dJSXF9mTw | `shwh` |
| 医学分词 CWS | https://pan.baidu.com/s/1bU3QoaGs2IxI34WBx7ibMQ | `yhek` |

也可以直接克隆代码仓库，`git clone https://github.com/king-yyf/CMeKG_tools.git`（模型仍需从上面的网盘下载）。

解压后的目录结构：

```
tools/CMeKG_tools-main/CMeKG/
├── medical_cws/
├── medical_ner/
└── medical_re/
```

缺失时日志会报模型加载失败，**知识库混合检索与问答主流程仍然可用**，仅实体覆盖通道的质量下降。

### 第三步：构建检索索引

```powershell
.\.venv\Scripts\python.exe scripts\build_hybrid_index.py
```

- 首次构建三个库约需 5~10 分钟，输出到 `data/index_cache/hybrid_v4_<库名>_<文档数>.pkl`（合计约 395 MB）
- 之后每次启动直接加载缓存，约 20 秒
- 修改了知识库数据后，用 `--rebuild` 强制重建：

```powershell
.\.venv\Scripts\python.exe scripts\build_hybrid_index.py --rebuild
```

索引缓存文件名包含文档数，数据量变化时会自动失效重建，无需手动清理。

### 第四步：验证

```powershell
.\.venv\Scripts\python.exe scripts\eval_retrieval.py
```

脚本会输出 Recall@1/5/10、MRR、nDCG 等指标。若没有评估集，先运行：

```powershell
.\.venv\Scripts\python.exe scripts\build_eval_dataset.py
```

## 访问地址

| 入口 | 地址 | 说明 |
|---|---|---|
| 完整前端界面 | `http://127.0.0.1:5173/ui/index.html` | **必须带 `/ui/index.html` 结尾** |
| 后端简版页面 | `http://127.0.0.1:8010/` | Django 自带对话页 |
| 对话 API | `POST http://127.0.0.1:8010/api/medical/chat/` | JSON：`{"content": "..."}` |

问答响应中除正文外还包含 `sources` 字段，列出命中的知识库条目（名称、所属库、相关度、内容摘要），用于结果溯源。

## 常见问题

1. **前端打开显示应用内 404**：确认地址完整为 `http://127.0.0.1:5173/ui/index.html`；路由已内置 `/index.html` 重定向，按 `Ctrl+F5` 强制刷新。
2. **8010 端口被占用**：
   ```powershell
   Stop-Process -Id (Get-NetTCPConnection -LocalPort 8010 -State Listen).OwningProcess -Force
   ```
3. **启动日志出现 `Some weights of BertForTokenClassification were not initialized`**：CMeKG 的 NER/CWS/RE 分类头为随机初始化（未微调），仅影响实体识别质量，不影响混合检索与问答主流程，可忽略。
4. **回答很短、没有引用知识库**：说明知识库或索引缺失。检查 `data/knowledge_bases/` 是否有数据、`data/index_cache/` 是否有 `hybrid_v4_*.pkl`。
5. **图片 404**：前端图片由 Django 通过 `/medical/` 映射到 `ui/public/medical/`，需保证后端在运行。
6. **前端 `npm run dev` 报 5173 端口占用**：说明已有一个实例在跑，直接访问即可，或先结束占用进程再启动。

## License

MIT，详见 `LICENSE`。
