import json
import os
import sys
import traceback
from typing import List, Dict, Any, Optional

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from apps.common.knowledge.knowledge_base import get_knowledge_base

class ResilientKnowledgeImporter:
    """弹性知识库导入器"""
    
    def __init__(self, json_file: str, chunk_size: int = 100):
        self.json_file = json_file
        self.chunk_size = chunk_size
        self.state_file = os.path.join(os.path.dirname(__file__), '../../../data/processed_kb/processing_state.json')
        self.log_file = os.path.join(os.path.dirname(__file__), '../../../data/processed_kb/import_log.txt')
        
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
            'total_processed': 0,
            'total_imported': 0,
            'errors': 0,
            'report_analysis': {'attempted': 0, 'imported': 0},
            'medicine_analysis': {'attempted': 0, 'imported': 0},
            'medical_service': {'attempted': 0, 'imported': 0}
        }
        
        # 确保状态和日志目录存在
        os.makedirs(os.path.dirname(self.state_file), exist_ok=True)
        
        # 加载上次的处理状态
        self.processed_lines = set()
        self.last_position = 0
        self.load_state()
    
    def load_state(self):
        """加载处理状态"""
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r', encoding='utf-8-sig') as f:
                    state = json.load(f)
                self.processed_lines = set(state.get('processed_lines', []))
                self.last_position = state.get('last_position', 0)
                print(f"加载上次处理状态: 已处理 {len(self.processed_lines)} 条，最后位置: {self.last_position}")
            except Exception as e:
                self.log_error(f"加载状态文件失败: {str(e)}")
                # 状态文件损坏，重新开始
                self.processed_lines = set()
                self.last_position = 0
    
    def save_state(self, current_position: int):
        """保存处理状态"""
        try:
            state = {
                'processed_lines': list(self.processed_lines),
                'last_position': current_position
            }
            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(state, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self.log_error(f"保存状态文件失败: {str(e)}")
    
    def log_error(self, message: str):
        """记录错误日志"""
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(f"{message}\n")
        except Exception:
            pass
        print(f"错误: {message}")
    
    def log_info(self, message: str):
        """记录信息日志"""
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(f"{message}\n")
        except Exception:
            pass
        print(message)
    
    def load_data_in_chunks(self):
        """分块加载数据"""
        try:
            with open(self.json_file, 'r', encoding='utf-8-sig') as f:
                # 移动到上次的位置
                f.seek(self.last_position)
                
                chunk = []
                current_position = self.last_position
                line_number = 0
                
                for line in f:
                    line_number += 1
                    current_position += len(line.encode('utf-8'))
                    
                    # 跳过已处理的行
                    if str(line_number) in self.processed_lines:
                        continue
                    
                    # 尝试解析JSON
                    try:
                        # 处理JSONL格式（每行一个JSON对象）
                        line = line.strip()
                        if line:
                            try:
                                obj = json.loads(line)
                                chunk.append((line_number, obj))
                            except json.JSONDecodeError as e:
                                self.log_error(f"解析行 {line_number} 失败: {str(e)}")
                                # 即使解析失败也要标记为已处理，避免重复处理
                                self.processed_lines.add(str(line_number))
                    except Exception as e:
                        self.log_error(f"处理行 {line_number} 失败: {str(e)}")
                        # 即使出错也要标记为已处理，避免重复处理
                        self.processed_lines.add(str(line_number))
                    
                    # 达到块大小，返回当前块
                    if len(chunk) >= self.chunk_size:
                        yield chunk, current_position
                        chunk = []
                
                # 处理最后一块
                if chunk:
                    yield chunk, current_position
        except Exception as e:
            self.log_error(f"加载数据失败: {str(e)}")
            yield [], 0
    
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
    
    def _import_to_knowledge_base(self, kb_name: str, item: Dict[str, Any]):
        """导入数据到知识库"""
        try:
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
            
            return True
        except Exception as e:
            self.log_error(f"导入知识库 {kb_name} 失败: {str(e)}")
            return False
    
    def process_chunk(self, chunk: List[tuple], current_position: int):
        """处理一个数据块"""
        for line_number, item in chunk:
            try:
                self.stats['total_processed'] += 1
                
                # 对每个知识库独立判断
                for kb_name, requirements in self.kb_requirements.items():
                    self.stats[kb_name]['attempted'] += 1
                    
                    # 检查是否符合入库标准
                    if self._meets_requirements(item, kb_name, requirements):
                        # 符合标准，导入
                        if self._import_to_knowledge_base(kb_name, item):
                            self.stats[kb_name]['imported'] += 1
                            self.stats['total_imported'] += 1
                            
                # 标记为已处理
                self.processed_lines.add(str(line_number))
                
                # 每处理100条保存一次状态
                if self.stats['total_processed'] % 100 == 0:
                    self.save_state(current_position)
                    self.log_info(f"已处理 {self.stats['total_processed']} 条，成功导入 {self.stats['total_imported']} 条")
                    
            except Exception as e:
                self.stats['errors'] += 1
                self.log_error(f"处理数据失败 (行 {line_number}): {str(e)}")
                # 即使出错也要标记为已处理，避免重复处理
                self.processed_lines.add(str(line_number))
    
    def process_in_chunks(self):
        """分块处理数据"""
        try:
            for chunk, current_position in self.load_data_in_chunks():
                if not chunk:
                    break
                
                self.process_chunk(chunk, current_position)
                
                # 保存状态
                self.save_state(current_position)
                
        except Exception as e:
            self.log_error(f"处理过程失败: {str(e)}")
            # 保存当前状态
            self.save_state(self.last_position)
        finally:
            # 处理完成，打印统计信息
            self.print_stats()
    
    def print_stats(self):
        """打印统计信息"""
        print("\n" + "="*60)
        print("知识库导入统计")
        print("="*60)
        print(f"总处理数据: {self.stats['total_processed']}")
        print(f"成功导入: {self.stats['total_imported']}")
        print(f"错误数: {self.stats['errors']}")
        
        for kb_name, stats in self.stats.items():
            if kb_name in ['total_processed', 'total_imported', 'errors']:
                continue
            print(f"\n{kb_name}:")
            print(f"  尝试导入: {stats['attempted']}")
            print(f"  成功导入: {stats['imported']}")
            if stats['attempted'] > 0:
                rate = stats['imported'] / stats['attempted'] * 100
                print(f"  通过率: {rate:.1f}%")
        
        print("\n处理完成！")

def import_medical_data():
    """导入医疗数据"""
    json_file = os.path.join(os.path.dirname(__file__), '../../../medical.json')
    if os.path.exists(json_file):
        print(f"开始处理医疗数据: {json_file}")
        importer = ResilientKnowledgeImporter(json_file, chunk_size=50)
        importer.process_in_chunks()
    else:
        print("medical.json 文件不存在")

def import_drug_data():
    """导入药品数据"""
    json_file = os.path.join(os.path.dirname(__file__), '../../../drug.json')
    if os.path.exists(json_file):
        print(f"开始处理药品数据: {json_file}")
        importer = ResilientKnowledgeImporter(json_file, chunk_size=50)
        importer.process_in_chunks()
    else:
        print("drug.json 文件不存在")

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='弹性知识库导入器')
    parser.add_argument('--input', type=str, help='输入文件路径')
    args = parser.parse_args()
    
    if args.input:
        print(f"开始处理指定文件: {args.input}")
        importer = ResilientKnowledgeImporter(args.input, chunk_size=50)
        importer.process_in_chunks()
    else:
        print("开始导入医疗数据...")
        import_medical_data()
        
        print("\n开始导入药品数据...")
        import_drug_data()

if __name__ == "__main__":
    main()
