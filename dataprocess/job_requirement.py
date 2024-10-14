import pandas as pd 

class ExtractJobRequirement:
    def __init__(self, path: str) -> None:
        self.path = path
        self.job_data = None
        self.job_number = None
        self.job_title = None
        self.company_name = None
        self.job_link = None
        self.responsibility = None
        self.qualification_min = None
        self.qualification_advanced = None
        self.job_dict = None
        
    def extract_job_data(self) -> None:
        job_data = pd.read_excel(io=self.path)
        self.job_data = job_data
        self.job_number = job_data['Number']
        self.job_title = job_data['Job Title']
        self.company_name = job_data['Company Name']
        self.job_link = job_data['Link']
        self.responsibility = job_data['Responsibility']
        self.qualification_min = job_data['Qualification(Min)']
        self.qualification_advanced = job_data['Qualification(Advanced)']

    def clear_up(self) -> None:
        job_dict = {}
        for _, row in self.job_data.iterrows():
            job_dict[row['Number']] = {
                'Job Title': row['Job Title'],
                'Company Name': row['Company Name'],
                'Link': row['Link'],
                'Qualification(Min)': row['Qualification(Min)']
            }
        self.job_dict = job_dict
