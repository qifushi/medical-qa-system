import json
import os
import sys
from typing import List, Dict, Any

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from apps.common.knowledge.knowledge_base import get_knowledge_base

class SelectiveKnowledgeImporter:
    """选择性知识库导入器"""
    
    def __init__(self, json_file: str):
        self.json_file = json_file
        
        # 初始化知识库
        self.knowledge_bases = {
            'report_analysis': get_knowledge_base('report_analysis'),
            'medicine_analysis': get_knowledge_base('medicine_analysis'),
            'medical_service': get_knowledge_base('medical_service')
        }
        
        # 定义每个知识库需要的最低内容标准
        self.kb_requirements = {
            'report_analysis': {
                'required_fields': ['check'],  # 必须有的字段
                'min_content_length': 10,      # 最小内容长度
                'min_items': 1,                 # 最少项目数（如果是列表）
                'quality_check': self._check_report_quality  # 自定义质量检查
            },
            'medicine_analysis': {
                'required_fields': ['recommand_drug'],
                'min_content_length': 5,
                'min_items': 1,
                'quality_check': self._check_medicine_quality
            },
            'medical_service': {
                'required_fields': ['cure_way'],
                'min_content_length': 10,
                'min_items': 1,
                'quality_check': self._check_service_quality
            }
        }
        
        # 统计信息
        self.stats = {
            'report_analysis': {'attempted': 0, 'imported': 0, 'skipped_reasons': {}},
            'medicine_analysis': {'attempted': 0, 'imported': 0, 'skipped_reasons': {}},
            'medical_service': {'attempted': 0, 'imported': 0, 'skipped_reasons': {}}
        }
    
    def load_data(self) -> List[Dict[str, Any]]:
        """加载JSON数据"""
        try:
            with open(self.json_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 处理多个JSON对象拼接的情况
            data = []
            # 分割JSON对象
            objects = content.split('}\n{')
            for i, obj_str in enumerate(objects):
                if i == 0:
                    obj_str = obj_str + '}'
                elif i == len(objects) - 1:
                    obj_str = '{' + obj_str
                else:
                    obj_str = '{' + obj_str + '}'
                
                try:
                    obj = json.loads(obj_str)
                    data.append(obj)
                except Exception as e:
                    print(f"解析JSON对象失败: {str(e)}")
            
            return data
        except Exception as e:
            print(f"加载数据失败: {str(e)}")
            return []
    
    def classify_and_import(self):
        """分类并导入数据"""
        data = self.load_data()
        print(f"加载了 {len(data)} 条医疗数据")
        
        for i, item in enumerate(data):
            print(f"\n处理第 {i+1} 条数据: {item.get('name', '无标题')}")
            
            # 对每个知识库独立判断
            for kb_name, requirements in self.kb_requirements.items():
                self.stats[kb_name]['attempted'] += 1
                
                # 检查是否符合入库标准
                if self._meets_requirements(item, kb_name, requirements):
                    # 符合标准，导入
                    self._import_to_knowledge_base(kb_name, item)
                    self.stats[kb_name]['imported'] += 1
                    print(f"  ✅ 导入 {kb_name}: {self._get_summary(item, kb_name)}")
                else:
                    # 记录跳过原因
                    reason = self._get_skip_reason(item, kb_name, requirements)
                    self.stats[kb_name]['skipped_reasons'][reason] = self.stats[kb_name]['skipped_reasons'].get(reason, 0) + 1
        
        self.print_stats()
        print("数据导入完成")
    
    def _meets_requirements(self, item: Dict, kb_name: str, requirements: Dict) -> bool:
        """检查是否满足入库要求"""
        
        field = requirements['required_fields'][0]
        
        # 1. 字段必须存在
        if field not in item:
            return False
        
        field_value = item[field]
        
        # 2. 字段不能为空
        if not field_value:
            return False
        
        # 3. 根据类型检查内容质量
        if isinstance(field_value, list):
            # 列表类型：检查长度和内容质量
            if len(field_value) < requirements['min_items']:
                return False
            
            # 检查列表项是否真的有内容
            valid_items = [v for v in field_value if v and len(str(v).strip()) > 2]
            if len(valid_items) < requirements['min_items']:
                return False
            
            # 合并内容用于长度检查
            content = ' '.join(str(v) for v in valid_items)
            
        elif isinstance(field_value, str):
            # 字符串类型：检查长度
            if len(field_value.strip()) < requirements['min_content_length']:
                return False
            content = field_value
        else:
            # 其他类型
            content = str(field_value)
            if len(content) < requirements['min_content_length']:
                return False
        
        # 4. 自定义质量检查
        if requirements.get('quality_check'):
            if not requirements['quality_check'](item, field, content):
                return False
        
        return True
    
    def _check_report_quality(self, item: Dict, field: str, content: str) -> bool:
        """检查报告质量"""
        # 检查是否包含真正的检查项目
        check_keywords = ['CT', 'MRI', 'X线', 'B超', '血常规', '尿常规', 
                         '生化', '病理', '心电图', '内镜']
        
        # 检查内容中是否包含这些关键词
        has_keyword = any(kw in content for kw in check_keywords)
        
        # 或者检查是否是列表且有多个项目
        if isinstance(item[field], list) and len(item[field]) >= 3:
            return True
        
        return has_keyword
    
    def _check_medicine_quality(self, item: Dict, field: str, content: str) -> bool:
        """检查药品质量"""
        # 药品相关关键词
        drug_keywords = ['片', '胶囊', '注射液', '口服液', '膏', '剂',
                        '抗生素', '降压', '降糖', '消炎', '止痛']
        
        # 检查是否包含药品特征
        has_keyword = any(kw in content for kw in drug_keywords)
        
        # 检查是否有具体用法
        has_usage = '用法' in content or '用量' in content or '服用' in content
        
        return has_keyword or has_usage
    
    def _check_service_quality(self, item: Dict, field: str, content: str) -> bool:
        """检查服务质量"""
        # 治疗相关关键词
        service_keywords = ['手术', '治疗', '康复', '护理', '住院',
                           '方案', '方法', '步骤', '流程']
        
        has_keyword = any(kw in content for kw in service_keywords)
        
        # 检查是否有详细描述
        has_detail = len(content) > 50
        
        return has_keyword and has_detail
    
    def _get_skip_reason(self, item: Dict, kb_name: str, requirements: Dict) -> str:
        """获取跳过原因"""
        field = requirements['required_fields'][0]
        
        if field not in item:
            return "字段不存在"
        
        if not item[field]:
            return "字段为空"
        
        if isinstance(item[field], list):
            if len(item[field]) < requirements['min_items']:
                return f"列表项不足({len(item[field])} < {requirements['min_items']})"
            
            valid_items = [v for v in item[field] if v and len(str(v).strip()) > 2]
            if len(valid_items) < requirements['min_items']:
                return "有效内容不足"
        
        elif isinstance(item[field], str):
            if len(item[field].strip()) < requirements['min_content_length']:
                return f"内容太短({len(item[field].strip())} < {requirements['min_content_length']})"
        
        return "质量检查未通过"
    
    def _get_summary(self, item: Dict, kb_name: str) -> str:
        """获取内容摘要"""
        field = self.kb_requirements[kb_name]['required_fields'][0]
        value = item[field]
        
        if isinstance(value, list):
            return f"[{'、'.join(str(v)[:20] for v in value[:3])}...]"
        else:
            return str(value)[:50] + "..."
    
    def _import_to_knowledge_base(self, kb_name: str, item: Dict[str, Any]):
        """导入数据到知识库"""
        kb = self.knowledge_bases[kb_name]
        
        # 生成实体ID
        entity_id = "medical_" + str(hash(item.get('name', '') + str(item.get('_id', ''))))
        
        # 确定实体类型
        entity_type = {
            'report_analysis': 'report',
            'medicine_analysis': 'medicine',
            'medical_service': 'medical_service'
        }[kb_name]
        
        # 构建实体属性
        properties = {
            'source': 'medical_json',
            'name': item.get('name', ''),
            'desc': item.get('desc', ''),
            'category': item.get('category', []),
            'prevent': item.get('prevent', ''),
            'cause': item.get('cause', ''),
            'symptom': item.get('symptom', []),
            'yibao_status': item.get('yibao_status', ''),
            'get_prob': item.get('get_prob', ''),
            'get_way': item.get('get_way', ''),
            'acompany': item.get('acompany', []),
            'cure_department': item.get('cure_department', []),
            'cure_way': item.get('cure_way', []),
            'cure_lasttime': item.get('cure_lasttime', ''),
            'cured_prob': item.get('cured_prob', ''),
            'cost_money': item.get('cost_money', ''),
            'check': item.get('check', []),
            'recommand_drug': item.get('recommand_drug', []),
            'drug_detail': item.get('drug_detail', []),
            'do_eat': item.get('do_eat', []),
            'not_eat': item.get('not_eat', []),
            'recommand_eat': item.get('recommand_eat', [])
        }
        
        # 添加实体到知识库
        kb.add_entity(
            entity_id=entity_id,
            entity_type=entity_type,
            entity_name=item.get('name', '无标题'),
            properties=properties
        )
    
    def print_stats(self):
        """打印详细统计"""
        print("\n" + "="*60)
        print("知识库导入统计")
        print("="*60)
        
        for kb_name, stats in self.stats.items():
            print(f"\n📊 {kb_name}:")
            print(f"  尝试导入: {stats['attempted']}")
            print(f"  成功导入: {stats['imported']}")
            
            if stats['attempted'] > 0:
                rate = stats['imported'] / stats['attempted'] * 100
                print(f"  通过率: {rate:.1f}%")
            
            if stats['skipped_reasons']:
                print("  跳过原因:")
                for reason, count in stats['skipped_reasons'].items():
                    print(f"    - {reason}: {count}次")

def import_medical_data():
    """导入医疗数据"""
    json_file = os.path.join(os.path.dirname(__file__), '../../../medical.json')
    importer = SelectiveKnowledgeImporter(json_file)
    importer.classify_and_import()

def import_drug_data():
    """导入药品数据"""
    json_file = os.path.join(os.path.dirname(__file__), '../../../drug.json')
    if os.path.exists(json_file):
        importer = SelectiveKnowledgeImporter(json_file)
        importer.classify_and_import()
    else:
        print("drug.json 文件不存在")

def main():
    """主函数"""
    print("开始导入医疗数据...")
    import_medical_data()
    
    print("\n开始导入药品数据...")
    import_drug_data()

if __name__ == "__main__":
    main()
