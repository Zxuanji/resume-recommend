
from dataprocess.job_requirement import ExtractJobRequirement

from sentence_transformers import SentenceTransformer, util # type: ignore

class CalculateSimilarity:
    def __init__(self, job_requirement: ExtractJobRequirement, resume_experience: str) -> None:
        self.job_requirement = job_requirement
        self.resume_experience = resume_experience
        self.model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    def calculate_similarity(self):
        # job_requirements = dict(zip(self.job_requirement.job_link, self.job_requirement.qualification_min))
        resume_embedding = self.model.encode(self.resume_experience, convert_to_tensor=True)
        
        # matching_report = []
        
        # for job, requirements in job_requirements.items():
        #     job_embedding = self.model.encode(str(requirements), convert_to_tensor=True)
        #     similarity_score = util.pytorch_cos_sim(resume_embedding, job_embedding).item()
        #     matching_report.append((job, similarity_score))
        
        # matching_report.sort(key=lambda x: x[1], reverse=True)
        
        # print("Resume Matching Results (BERT):")
        # for job, score in matching_report:
        #     print(f"Job: {job}, Similarity Score: {score:.4f}")
        # print(matching_report)
        similarity_dict = {}
        
        for job_number, job_info in self.job_requirement.job_dict.items():
            qualification_min = job_info['Qualification(Min)']
            job_embedding = self.model.encode(str(qualification_min), convert_to_tensor=True)
            similarity_score = util.pytorch_cos_sim(resume_embedding, job_embedding).item()
            similarity_dict[job_number] = {
                'Job Title': job_info['Job Title'],
                'Company Name': job_info['Company Name'],
                'Link': job_info['Link'],
                'Qualification(Min)': qualification_min,
                'Similarity Score': similarity_score
            }
            
        sorted_similarity = dict(sorted(similarity_dict.items(), key=lambda item: item[1]['Similarity Score'], reverse=True)[:8])
        # print("Top 8 Resume Matching Results (BERT):")
        # for job_number, job_info in sorted_similarity.items():
        #     print(f"Job: {job_info['Job Title']}, Similarity Score: {job_info['Similarity Score']:.4f}")

        return sorted_similarity

            

        

