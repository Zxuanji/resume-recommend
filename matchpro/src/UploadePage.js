import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './UploadPage.css';

function UploadPage() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [isUploadComplete, setIsUploadComplete] = useState(false);
  const [jobRecommendations, setJobRecommendations] = useState(null);
  const fileInputRef = React.createRef();
  const navigate = useNavigate();

  // 处理文件选择
  const handleFileChange = (event) => {
    if (event.target.files && event.target.files.length > 0) {
      const file = event.target.files[0];
      setSelectedFile(file);
      setUploadProgress(0); // 重置进度条
      setIsUploadComplete(false); // 重置上传完成状态
      handleFileUpload(file); // 选择文件后立即上传
    } else {
      alert('Please select a valid file.');
    }
  };

  // 触发文件选择框
  const handleButtonClick = () => {
    fileInputRef.current.click(); // 触发隐藏的文件输入框的点击事件
  };

  // 文件上传处理
  const handleFileUpload = (file) => {
    if (!file) {
      alert('Please select a file first');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    const xhr = new XMLHttpRequest();
    xhr.open('POST', 'http://localhost:5000/upload', true);
    xhr.setRequestHeader("Accept", "application/json");

    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4 && xhr.status == 200) {
            console.log(xhr.responseText);
        } else if (xhr.readyState == 4) {
            console.error('Error:', xhr.status, xhr.statusText);
        }
};
    
    // 监听上传进度事件
    xhr.upload.addEventListener('progress', (event) => {
      if (event.lengthComputable) {
        const percentComplete = Math.round((event.loaded / event.total) * 100);
        setUploadProgress(percentComplete);
      }
    });
    
    // 监听上传完成事件
    xhr.addEventListener('load', () => {
      if (xhr.status === 200) {
        console.log('Upload Successful:', xhr.responseText);
        const jobData = JSON.parse(xhr.responseText);

        const{ id, job_data} = jobData;

        if(id){
          setJobRecommendations(jobData);
          setUploadProgress(100);
          setIsUploadComplete(true);
        }else{
          alert('Upload response did not contain a unique ID');
          setUploadProgress(0);
        }  
      } else {
        alert('Upload failed');
        setUploadProgress(0);
      }
    });
    
    // 监听错误事件
    xhr.addEventListener('error', () => {
      console.error('Error during file upload:', xhr.statusText);
      alert('An error occurred while uploading the file');
      setUploadProgress(0);
    });
    
    xhr.send(formData);
  };

  // 点击“Analyze now”按钮处理
  const handleAnalyzeClick = () => {
    if (isUploadComplete && jobRecommendations) {
      const {id, job_data} = jobRecommendations;
      if(id){
        navigate('/Results',{state:{id, job_data}});
      }else {
        alert('Missing unique ID for analysis');
      }
    } else {
      alert('Please wait for the file to finish uploading before proceeding.');
    }
  };

  // 组件渲染部分
  return (
    <div className="App">
      <header className="App-header">
        <h1>MatchPro</h1>
      </header>

      <div className='upload-container'>
        <h2>Improve your career with MatchPro</h2>

        <div className='dropZone'>
          <img src='/pdf.png' alt="File upload icon" className="upload-icon" />

          <p>Drag and drop font files to upload</p>
          <p>Support: .pdf, .txt, .word format files, maximum file size 20MB.</p>

          <button className="custom-file-upload" onClick={handleButtonClick}>
            Select files
          </button>

          <input
            type="file"
            ref={fileInputRef}
            style={{ display: 'none' }}
            onChange={handleFileChange}
          />
        </div>
        
        {selectedFile && (
          <div className='file-upload-status'>
            <div className='file-info'>
              <span>📄 {selectedFile.name}</span>
              <span>{uploadProgress}%</span>
            </div>
            <div className='progress-bar'>
              <div className='progress' style={{ width: `${uploadProgress}%` }}></div>
            </div>
          </div>
        )}
        
        <div className='analyze-button-container'>
          <button 
            className='analyze-button' 
            onClick={handleAnalyzeClick}
            disabled={!isUploadComplete} // 上传完成后按钮才可用
          >
            Analyze now!
          </button>
        </div>
      </div>
    </div>
  );
}

export default UploadPage;
