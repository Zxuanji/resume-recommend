import os
import sys

if __name__ == "__main__":
    curr_dir = os.path.abspath(os.path.join(__file__, ".."))
    os.chdir(curr_dir)
    lib_path = os.path.abspath(os.path.join(curr_dir))
    sys.path.append(lib_path)

from dataprocess.job_requirement import ExtractJobRequirement
from dataprocess.resume import ExtractResume
from similarity.job_similarity import CalculateSimilarity


# 打印PDF中的文本内容
# print(sections)

pdf_path = 'sample.pdf'
pdf_text = ExtractResume.extract_resume(pdf_path)
sections = ExtractResume.extract_experience(pdf_text)

internship_experience = sections['internship experience']
project_experience = sections['project experience']

ejr = ExtractJobRequirement(path="dataset/job_requirement.xlsx")
ejr.extract_job_data()
ejr.clear_up()

resume_experience = internship_experience + " " + project_experience

cal = CalculateSimilarity(ejr, resume_experience)
cal.calculate_similarity()