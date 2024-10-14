import sys

curr_dir = os.path.abspath(os.path.join(__file__, ".."))
os.chdir(curr_dir)
lib_path = os.path.abspath(os.path.join(curr_dir))
sys.path.append(lib_path)

from flask import Flask, Response, request, jsonify
from dataprocess.job_requirement import ExtractJobRequirement
from dataprocess.resume import ExtractResume
from similarity.job_similarity import CalculateSimilarity
import json
import os
app = Flask(__name__)

UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route("/")
def index():
    return Response(json.dumps({
        "status": True,
        "code": 200,
        "message": "It is working!"}), mimetype="application/json")

@app.route("/upload", methods=['post'])
def upload_pdf():
    if 'file' not in request.files():
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == "":
        return jsonify({'error': 'No selected file'}), 400
    
    if file and file.filename.endswith('.pdf'):
        # 暂时的逻辑是保存在项目本身，后续要保存到数据库需单独处理
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        pdf_text = ExtractResume.extract_resume(filepath)
        sections = ExtractResume.extract_experience(pdf_text)
        
        internship_experience = sections['internship experience']
        project_experience = sections['project experience']
        
        ejr = ExtractJobRequirement(path="dataset/job_requirement.xlsx")
        ejr.extract_job_data()
        ejr.clear_up()
        
        resume_experience = internship_experience + " " + project_experience
        
        cal = CalculateSimilarity(ejr, resume_experience)
        return jsonify(cal.calculate_similarity())
    else:
        return jsonify({'error': 'Invalid file format, please upload a PDF'}), 400

if __name__ == '__main__':
    app.run(debug=True)