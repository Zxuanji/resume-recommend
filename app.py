import sys
import os

curr_dir = os.path.abspath(os.path.join(__file__, ".."))
os.chdir(curr_dir)
lib_path = os.path.abspath(os.path.join(curr_dir))
sys.path.append(lib_path)

from flask import Flask, Response, request, jsonify, send_file
from flask_cors import CORS, cross_origin
from dataprocess.job_requirement import ExtractJobRequirement
from dataprocess.resume import ExtractResume
from similarity.job_similarity import CalculateSimilarity
from graph_generate.kg_visualization import KGVisualization
import io
import json
import uuid
import sqlite3

app = Flask(__name__)
app.secret_key = 'Selladokuk980820'  # 必须添加以支持 session
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)

UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
    
kg_visualizer = KGVisualization()

@app.route("/")
def index():
    return Response(json.dumps({
        "status": True,
        "code": 200,
        "message": "It is working!"}), mimetype="application/json")

@app.route("/upload", methods=['POST', 'OPTIONS'])
@cross_origin(origin='http://localhost:3000', headers=['Content-Type', 'Authorization'], supports_credentials=True)
def upload_pdf():
    # 处理 OPTIONS 预检请求
    if request.method == 'OPTIONS':
        response = Response()
        response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
        response.headers.add("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
        return response, 200

    if 'file' not in request.files:
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

        unique_id = str(uuid.uuid4())
        job_ids=[]

        # 存储经验数据到数据库
        conn = sqlite3.connect('database/experience_job_data.db')
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO experience_data (id, experience)
        VALUES (?, ?)
        ''', (unique_id, resume_experience))
        conn.commit()

        cal = CalculateSimilarity(ejr, resume_experience)
        similarity_result = cal.calculate_similarity()
        
        job_data = [
            {
                "id": str(uuid.uuid4()),  # 每个职位单独生成一个 ID
                "title": job_info["Job Title"],
                "company": job_info["Company Name"],
                "website": job_info["Link"],
                "qualification": job_info["Qualification(Min)"]
            }
            for job_info in similarity_result.values()
        ]

        # 存储职位数据到数据库
        for job in job_data:
            cursor.execute('''
            INSERT INTO job_data (id, title, company, website, qualification)
            VALUES (?, ?, ?, ?, ?)
            ''', (job['id'], job['title'], job['company'], job['website'], job['qualification']))
            
            job_ids.append(job['id'])
            
        job_ids_str = ",".join(job_ids)
        cursor.execute('''
        UPDATE experience_data SET job_ids = ? WHERE id = ?
        ''', (job_ids_str, unique_id))
        
        conn.commit()
        conn.close()

        return jsonify({'job_data': job_data, 'id': unique_id}), 200
    else:
        return jsonify({'error': 'Invalid file format, please upload a PDF'}), 400

@app.route('/get-graph-data', methods=['GET'])
def generate_graph_image():
    unique_id = request.args.get('id')
    if unique_id is None:
        return jsonify({"error": "No job data available. Please upload a PDF first."}), 400

    # 从数据库中获取数据
    conn = sqlite3.connect('database/experience_job_data.db')
    cursor = conn.cursor()

    cursor.execute('SELECT experience, job_ids FROM experience_data WHERE id = ?', (unique_id,))
    experience_row = cursor.fetchone()

    if experience_row is None:
        return jsonify({"error": "Experience data not found"}), 400

    uploaded_experience_text = experience_row[0]
    job_ids_str = experience_row[1]
    job_ids = job_ids_str.split(",") if job_ids_str else []

    uploaded_job_data = []
    for job_id in job_ids:
        cursor.execute('SELECT title, company, website, qualification FROM job_data WHERE id = ?', (job_id,))
        job_row = cursor.fetchone()
        if job_row:
            uploaded_job_data.append({
                "title": job_row[0],
                "company": job_row[1], 
                "website": job_row[2], 
                "qualification": job_row[3]
                })

    conn.close()

    if not uploaded_job_data or not uploaded_experience_text:
        return jsonify({"error": "No job data available. Please upload a PDF first."}), 400

    try:
        # 使用 Pyvis 生成 HTML 图表
        output_html_path = f"static/graphs/job_skill_graph_{unique_id}.html"
        kg_visualizer.generate_graph_image(unique_id, output_html = output_html_path)
        
        graph_url = f"/{output_html_path}"
        return jsonify({"graph_url": graph_url}), 200
    
    except Exception as e:
        print(f"Error generating graph image: {e}")
        return jsonify({"error": "Failed to generate graph image"}), 500

if __name__ == '__main__':
    app.run(debug=True)