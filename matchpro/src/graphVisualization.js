import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';

function GraphVisualization() {
    const location = useLocation();
    const [graphUrl, setGraphUrl] = useState(null);
    const uniqueId = location.state?.id;

    useEffect(() => {
        if (!uniqueId) return;

        fetch(`http://localhost:5000/get-graph-data?id=${uniqueId}`, {
            method: 'GET',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
            },
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (data.graph_url) {
                    // 将返回的图表 URL 设置为 state，以便在页面上展示
                    setGraphUrl(`http://localhost:5000${data.graph_url}`);
                }
            })
            .catch(error => {
                console.error('Error fetching the graph image:', error);
            });
    }, [uniqueId]);

    return (
        <div>
            {graphUrl ? (
                <iframe
                    src={graphUrl}
                    title="Graph Visualization"
                    style={{
                        width: '100%',
                        height: '600px',
                        border: '1px solid #ddd',
                        borderRadius: '10px'
                    }}
                />
            ) : (
                <p>Loading graph...</p>
            )}
        </div>
    );
}

export default GraphVisualization;
