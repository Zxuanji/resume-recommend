import pdfplumber
import re

class ExtractResume:
    @staticmethod
    def extract_resume(resume_path):
        text = ""
        with pdfplumber.open(resume_path) as pdf:
            # 遍历每一页
            for page in pdf.pages:
                text += page.extract_text()
        return text
    
    @staticmethod
    def extract_experience(resume_text):
        # 保留换行符，仅去掉其他多余空白字符
        text = re.sub(r'[ \t]+', ' ', resume_text.lower())
        
        sections = {
            'internship experience': "",
            'project experience': "",
        }
        
        section_headers = [
            ('project experience', re.compile(r'(project.*experience)', re.IGNORECASE)),
            ('internship experience', re.compile(r'(internship.*experience)', re.IGNORECASE)),
        ]
        
        section_positions = []
        
        # 查找每个section的起始位置
        for name, pattern in section_headers:
            match = pattern.search(text)
            if match:
                section_positions.append((name, match.start()))
        
        # 按照起始位置排序
        section_positions = sorted(section_positions, key=lambda x: x[1])
        
        # 提取每个部分的内容
        for i in range(len(section_positions)):
            section_name = section_positions[i][0]
            start_pos = section_positions[i][1]
            end_pos = section_positions[i + 1][1] if i + 1 < len(section_positions) else len(text)
            sections[section_name] = text[start_pos:end_pos].strip()
            
        for section, text in sections.items():
            sections[section] = ExtractResume.clean_text(text)
        
        return sections
    
    @staticmethod
    def clean_text(text):
        # 去掉 \uf0b7 符号
        text = re.sub(r'\uf0b7', '', text)
        # 去掉多余的换行符，将它们替换为单个空格或保留段落之间的分隔符
        # 替换连续的换行符为单个换行符，保留段落分隔
        text = re.sub(r'\n+', '\n', text)
        # 替换段落内部的换行符为单个空格（用于保持段落的连贯性）
        text = re.sub(r'(?<!\n)\n(?!\n)', ' ', text)
        # 去掉开头和结尾多余的空格
        text = text.strip()
        return text