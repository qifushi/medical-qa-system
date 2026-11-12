import os
import sys
import json
from typing import List, Dict, Tuple, Any

# 添加CMeKG路径到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../CMeKG')))

from CMeKG.medical_cws.run import medical_cws
from CMeKG.medical_ner.run import medical_ner
from CMeKG.medical_re.medical_re import load_model, get_triples

class ProcessingPipeline:
    """医疗文本处理流水线"""
    
    def __init__(self):
        self.cws_model = medical_cws()
        self.ner_model = medical_ner()
        self.re_model, self.predicate2id, self.id2predicate = load_model()
        self.output_dir = os.path.join(os.path.dirname(__file__), '../../../data/processed_data')
        os.makedirs(self.output_dir, exist_ok=True)
    
    def process_text(self, text: str) -> Dict[str, Any]:
        """处理单篇文本"""
        # 1. 分词
        words = self.cws_model.predict_sentence(text)
        
        # 2. 实体识别
        entities = self.ner_model.predict_sentence(text)
        
        # 3. 关系抽取
        triples = get_triples(text, self.re_model, self.predicate2id, self.id2predicate)
        
        # 4. 构建处理结果
        result = {
            'original_text': text,
            'words': words,
            'entities': entities,
            'triples': triples
        }
        
        return result
    
    def process_file(self, file_path: str) -> Dict[str, Any]:
        """处理文件"""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        processed_data = []
        for item in data:
            if 'content' in item:
                result = self.process_text(item['content'])
                processed_data.append({
                    **item,
                    'processed': result
                })
        
        # 保存处理结果
        output_file = os.path.join(self.output_dir, os.path.basename(file_path))
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(processed_data, f, ensure_ascii=False, indent=2)
        
        print(f"文件处理完成，结果保存到 {output_file}")
        return processed_data
    
    def process_directory(self, directory: str) -> List[Dict[str, Any]]:
        """处理目录"""
        processed_files = []
        
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.json'):
                    file_path = os.path.join(root, file)
                    print(f"处理文件: {file_path}")
                    result = self.process_file(file_path)
                    processed_files.append({
                        'file': file,
                        'data': result
                    })
        
        return processed_files

def get_processing_pipeline() -> ProcessingPipeline:
    """获取处理流水线实例"""
    return ProcessingPipeline()