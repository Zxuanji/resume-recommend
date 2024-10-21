import React from 'react';
import { useLocation } from 'react-router-dom';
import './Results.css';
import GraphVisualization from './graphVisualization'; // 导入上面写的图谱可视化组件

function Results() {
  const location = useLocation();
  const {id, job_data} = location.state || [];
  const uniqueId = location.state?.id; // 确保获取到 uniqueId

  console.log("Unique ID in Results component:", uniqueId);

  return (
    <div className="Results">
      <header className="Results-header">
        <h1>MatchPro</h1>
      </header>

      <div className="results-container">
        {/* 推荐职位部分 */}
        <h2>Job Recommended:</h2>
        <div className="job-recommendations">
          {/* 动态渲染推荐的工作卡片 */}
          {Array.isArray(job_data) && job_data.length > 0 ? (
            job_data.map((job, index) => (
              <div className="job-card" key={index}>
                <h3>{job.title}</h3>
                <p>{job.company}</p>
                <a href={job.website} target="_blank" rel="noopener noreferrer">
                  View the website
                </a>
              </div>
            ))
          ) : (
            <p>No job recommendations available.</p>
          )}
        </div>

        {/* 能力分析部分 */}
        <h2>Competence Analysis:</h2>
        {/* 使用 uniqueId 传递给 GraphVisualization */}
        {uniqueId && <GraphVisualization uniqueId={uniqueId} />}
      </div>
    </div>
  );
}

export default Results;
