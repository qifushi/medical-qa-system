"""
医疗问答数据智能分类导入脚本 v4 - 带断点续传功能
根据问答内容自动分类到三个知识库：
- report_analysis: 包含检查、检验、报告相关内容
- medicine_analysis: 包含药物、用药、处方相关内容  
- medical_service: 包含治疗方法、就医建议、手术等内容

支持断点续传：处理完的文件会被记录，重启后跳过已处理的文件
"""

import pandas as pd
import json
import os
import sys
from pathlib import Path
from typing import List, Dict, Any, Tuple
import chardet

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from apps.common.knowledge.knowledge_base import get_knowledge_base

class SmartMedicalQAImporter:
    """智能医疗问答分类导入器"""
    
    def __init__(self, reset_state=False):
        # 初始化三个知识库
        self.knowledge_bases = {
            'report_analysis': get_knowledge_base('report_analysis'),
            'medicine_analysis': get_knowledge_base('medicine_analysis'),
            'medical_service': get_knowledge_base('medical_service')
        }
        
        # 状态文件路径
        self.state_file = Path("data/processed_kb/qa_import_state.json")
        
        # 加载上次的处理状态
        self.processed_files = {}  # 改为字典，记录每个文件的处理行数
        if not reset_state:
            self.load_state()
        else:
            self.reset_state()
        
        # 每处理多少行保存一次
        self.save_interval = 1000  # 每 1000 行保存一次
        
        # 统计信息
        self.stats = {
            'total_rows': 0,
            'report_analysis': 0,
            'medicine_analysis': 0,
            'medical_service': 0,
            'multi_category': 0,
            'skipped': 0,
            'errors': 0
        }
        
        # 关键词分类
        self.keywords = {
            'report': [
                '检查', '检验', '化验', '报告', '检测',
                '血常规', '尿常规', 'CT', 'MRI', 'X 光', 'B 超',
                '心电图', '内镜', '病理', '活检',
                '血糖', '血脂', '血压', '白细胞', '红细胞', '血小板',
            ],
            'medicine': [
                '药', '用药', '处方', '服药', '吃药', '口服',
                '注射', '输液', '外敷', '涂抹',
                '抗生素', '消炎药', '止痛药', '降压药', '降糖药',
                '中药', '西药', '中成药',
                '剂量', '用量', '疗程', '副作用',
            ],
            'service': [
                '治疗', '手术', '疗法', '治疗方案',
                '医院', '科室', '医生', '就诊', '挂号',
                '住院', '门诊', '急诊', '病房',
                '康复', '护理', '复健',
            ]
        }
    
    def load_state(self):
        """加载处理状态"""
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r', encoding='utf-8') as f:
                    state = json.load(f)
                self.processed_files = state.get('processed_files', {})
                total_processed = sum(self.processed_files.values())
                print(f"✅ 加载上次处理状态：已处理 {len(self.processed_files)} 个文件，共 {total_processed} 行")
            except Exception as e:
                print(f"加载状态失败：{e}")
                self.processed_files = {}
    
    def save_state(self):
        """保存处理状态"""
        try:
            state = {'processed_files': self.processed_files}
            os.makedirs(self.state_file.parent, exist_ok=True)
            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(state, f, ensure_ascii=False, indent=2)
            total_processed = sum(self.processed_files.values())
            print(f"  💾 已保存进度：{len(self.processed_files)} 个文件，{total_processed} 行")
        except Exception as e:
            print(f"保存状态失败：{e}")
    
    def reset_state(self):
        """重置状态（用于重新开始）"""
        if self.state_file.exists():
            os.remove(self.state_file)
        self.processed_files = {}
        print("🔄 状态已重置，将重新处理所有文件")
    
    def classify_content(self, ask: str, answer: str) -> List[str]:
        """智能分类问答内容"""
        combined_text = (ask + answer).lower()
        categories = []
        
        report_score = sum(1 for kw in self.keywords['report'] if kw in combined_text)
        if report_score >= 1:
            categories.append('report_analysis')
        
        medicine_score = sum(1 for kw in self.keywords['medicine'] if kw in combined_text)
        if medicine_score >= 1:
            categories.append('medicine_analysis')
        
        service_score = sum(1 for kw in self.keywords['service'] if kw in combined_text)
        if service_score >= 1:
            categories.append('medical_service')
        
        if not categories and self.has_medical_content(ask, answer):
            categories.append('medical_service')
        
        return categories
    
    def has_medical_content(self, ask: str, answer: str) -> bool:
        """检查是否包含医疗相关内容"""
        medical_keywords = ['治疗', '药物', '检查', '诊断', '症状', '疾病', '医院', '医生']
        combined_text = ask + answer
        return any(kw in combined_text for kw in medical_keywords)
    
    def is_valid_content(self, text: str) -> bool:
        """检查内容是否有效"""
        if not text or not isinstance(text, str):
            return False
        text = text.strip()
        if len(text) < 10:
            return False
        invalid_patterns = ['暂无', '不知道', '不清楚', '无法确定']
        for pattern in invalid_patterns:
            if pattern in text:
                return False
        return True
    
    def extract_entities(self, answer: str, category: str) -> List[str]:
        """从回答中提取实体"""
        entities = []
        keyword_list = self.keywords.get('report' if category == 'report_analysis' else 
                                         'medicine' if category == 'medicine_analysis' else 'service', [])
        for kw in keyword_list:
            if kw in answer:
                entities.append(kw)
        return entities[:10]
    
    def add_to_knowledge_base(self, category: str, department: str, title: str, ask: str, answer: str):
        """添加到知识库"""
        try:
            kb = self.knowledge_bases[category]
            
            entity_type_map = {
                'report_analysis': 'report',
                'medicine_analysis': 'medicine',
                'medical_service': 'medical_service'
            }
            
            disease_name = title.strip() if title and len(title.strip()) > 1 else (ask[:30] if ask else '医疗咨询')
            
            properties = {
                'source': 'medical_qa_csv',
                'name': disease_name,
                'department': department.strip() if department else '',
                'title': title.strip() if title else '',
                'question': ask.strip() if ask else '',
                'answer': answer.strip() if answer else '',
            }
            
            if category == 'report_analysis':
                properties['check'] = self.extract_entities(answer, category)
            elif category == 'medicine_analysis':
                properties['recommand_drug'] = self.extract_entities(answer, category)
            elif category == 'medical_service':
                properties['cure_way'] = [answer.strip()] if answer else []
            
            entity_id = f"qa_{category}_{hash(department + title + ask)}"
            
            kb.add_entity(
                entity_id=entity_id,
                entity_type=entity_type_map[category],
                entity_name=properties['name'],
                properties=properties
            )
            
            return True
            
        except Exception as e:
            return False
    
    def process_csv_file(self, csv_file: Path) -> Tuple[int, int, int]:
        """处理单个 CSV 文件"""
        file_key = str(csv_file)
        
        # 获取上次处理的行数
        last_processed_line = self.processed_files.get(file_key, 0)
        
        if last_processed_line > 0:
            print(f"\n⏭️  继续处理文件：{csv_file.name} (从第 {last_processed_line + 1} 行开始)")
        else:
            print(f"\n处理文件：{csv_file}")
        
        report_count = 0
        medicine_count = 0
        service_count = 0
        
        try:
            encoding = detect_file_encoding(csv_file)
            print(f"  检测编码：{encoding}")
            
            df = pd.read_csv(csv_file, encoding=encoding if encoding else 'gbk')
            print(f"  总行数：{len(df)}")
            
            # 从上次处理的位置继续
            start_line = last_processed_line
            if start_line >= len(df):
                print(f"  ✅ 文件已全部处理完毕")
                self.processed_files[file_key] = len(df)
                return 0, 0, 0
            
            print(f"  从第 {start_line + 1} 行开始处理...")
            
            for idx in range(start_line, len(df)):
                row = df.iloc[idx]
                self.stats['total_rows'] += 1
                
                try:
                    department = str(row.get('department', ''))
                    title = str(row.get('title', ''))
                    ask = str(row.get('ask', ''))
                    answer = str(row.get('answer', ''))
                    
                    if not self.is_valid_content(ask) or not self.is_valid_content(answer):
                        self.stats['skipped'] += 1
                        continue
                    
                    if not self.has_medical_content(ask, answer):
                        self.stats['skipped'] += 1
                        continue
                    
                    categories = self.classify_content(ask, answer)
                    
                    if not categories:
                        self.stats['skipped'] += 1
                        continue
                    
                    for category in categories:
                        if self.add_to_knowledge_base(category, department, title, ask, answer):
                            if category == 'report_analysis':
                                report_count += 1
                                self.stats['report_analysis'] += 1
                            elif category == 'medicine_analysis':
                                medicine_count += 1
                                self.stats['medicine_analysis'] += 1
                            elif category == 'medical_service':
                                service_count += 1
                                self.stats['medical_service'] += 1
                    
                    if len(categories) > 1:
                        self.stats['multi_category'] += 1
                    
                except Exception as e:
                    self.stats['errors'] += 1
                
                # 每处理 save_interval 行保存一次状态
                current_line = idx + 1
                if current_line % self.save_interval == 0:
                    self.processed_files[file_key] = current_line
                    self.save_state()
                    print(f"  📊 已处理到第 {current_line} 行，导入 {report_count + medicine_count + service_count} 条")
            
            # 标记为已完成
            self.processed_files[file_key] = len(df)
            
            total = report_count + medicine_count + service_count
            print(f"  ✅ 成功导入：{total} 条")
            print(f"     - report_analysis: {report_count}")
            print(f"     - medicine_analysis: {medicine_count}")
            print(f"     - medical_service: {service_count}")
            
        except Exception as e:
            print(f"  ❌ 处理失败：{e}")
        
        return report_count, medicine_count, service_count
    
    def process_all_files(self):
        """处理所有 CSV 文件"""
        base_path = Path(__file__).resolve().parent / "Data_数据"
        csv_files = list(base_path.glob("**/*.csv"))
        
        print("="*60)
        print("开始智能分类导入医疗问答数据 v4 (带断点续传)")
        print("="*60)
        print(f"找到 {len(csv_files)} 个 CSV 文件")
        if self.processed_files:
            print(f"已处理 {len(self.processed_files)} 个文件，将跳过")
        print()
        
        total_report = 0
        total_medicine = 0
        total_service = 0
        
        for csv_file in csv_files:
            r, m, s = self.process_csv_file(csv_file)
            total_report += r
            total_medicine += m
            total_service += s
            
            # 每处理一个文件保存一次状态
            self.save_state()
        
        self.print_stats(total_report, total_medicine, total_service)
    
    def print_stats(self, total_report: int, total_medicine: int, total_service: int):
        """打印统计信息"""
        print("\n" + "="*60)
        print("最终统计")
        print("="*60)
        print(f"总处理数据：{self.stats['total_rows']}")
        print(f"跳过：{self.stats['skipped']}")
        print(f"错误：{self.stats['errors']}")
        print(f"\n成功导入知识库:")
        print(f"  📊 report_analysis:    {total_report} 条 (检查报告)")
        print(f"  💊 medicine_analysis:  {total_medicine} 条 (药品推荐)")
        print(f"  🏥 medical_service:    {total_service} 条 (医疗服务)")
        print(f"\n跨类别数据：{self.stats['multi_category']} 条")
        print("\n处理完成！")
        print("\n💡 提示：如果需要重新处理所有文件，请运行:")
        print("   python import_medical_qa_smart_v4.py --reset")

def detect_file_encoding(file_path: Path) -> str:
    """检测文件编码"""
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read(100000))
    return result['encoding']

def main():
    import argparse
    parser = argparse.ArgumentParser(description='医疗问答数据智能分类导入器')
    parser.add_argument('--reset', action='store_true', help='重置状态，重新处理所有文件')
    args = parser.parse_args()
    
    importer = SmartMedicalQAImporter(reset_state=args.reset)
    importer.process_all_files()

if __name__ == "__main__":
    main()
