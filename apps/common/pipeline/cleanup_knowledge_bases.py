import json
import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

class KnowledgeBaseCleaner:
    """知识库清理器"""
    
    def __init__(self):
        self.knowledge_bases_dir = os.path.join(os.path.dirname(__file__), '../../../data/knowledge_bases')
    
    def cleanup_knowledge_base(self, kb_name: str, min_items: int, field_name: str):
        """清理知识库"""
        kb_dir = os.path.join(self.knowledge_bases_dir, kb_name)
        entities_file = os.path.join(kb_dir, 'entities.json')
        
        if not os.path.exists(entities_file):
            print(f"{kb_name} 知识库文件不存在")
            return
        
        # 读取现有数据
        with open(entities_file, 'r', encoding='utf-8') as f:
            try:
                entities = json.load(f)
            except json.JSONDecodeError as e:
                print(f"解析 {kb_name} 知识库文件失败: {str(e)}")
                return
        
        print(f"清理前 {kb_name} 知识库中有 {len(entities)} 个实体")
        
        # 清理不符合条件的实体
        cleaned_entities = {}
        for entity_id, entity in entities.items():
            if field_name in entity:
                field_value = entity[field_name]
                if isinstance(field_value, list) and len(field_value) >= min_items:
                    cleaned_entities[entity_id] = entity
        
        print(f"清理后 {kb_name} 知识库中有 {len(cleaned_entities)} 个实体")
        
        # 写回清理后的数据
        with open(entities_file, 'w', encoding='utf-8') as f:
            json.dump(cleaned_entities, f, ensure_ascii=False, indent=2)
        
        print(f"{kb_name} 知识库清理完成")
    
    def cleanup_all(self):
        """清理所有知识库"""
        # 清理报告分析知识库：检查字段至少有2个项目
        self.cleanup_knowledge_base('report_analysis', 2, 'check')
        
        # 清理药品分析知识库：药物推荐字段至少有2个项目
        self.cleanup_knowledge_base('medicine_analysis', 2, 'recommand_drug')
        
        # 清理医疗服务知识库：治疗方法字段至少有2个项目
        self.cleanup_knowledge_base('medical_service', 2, 'cure_way')

def main():
    """主函数"""
    cleaner = KnowledgeBaseCleaner()
    cleaner.cleanup_all()

if __name__ == "__main__":
    main()
