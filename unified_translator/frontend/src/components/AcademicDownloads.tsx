import React from 'react';

const AcademicDownloads: React.FC = () => {
  return (
    <div style={{
      marginTop: '40px',
      padding: '20px',
      backgroundColor: '#f9f9f9',
      borderRadius: '8px'
    }}>
      <h2>📄 Academic Downloads</h2>
      <p>
        For peer review, citation, and academic distribution, you may download 
        the official methodology and license documents below:
      </p>
      <div style={{ marginTop: '20px' }}>
        <a 
          href="/downloads/Brett_Methodology.pdf" 
          download 
          className="download-button"
          style={{
            display: 'inline-block',
            padding: '10px 20px',
            backgroundColor: '#007bff',
            color: 'white',
            textDecoration: 'none',
            borderRadius: '5px',
            marginRight: '10px',
            marginBottom: '10px'
          }}
        >
          📘 Brett Methodology PDF
        </a>
        <br />
        <a 
          href="/downloads/Brett_License.pdf" 
          download 
          className="download-button"
          style={{
            display: 'inline-block',
            padding: '10px 20px',
            backgroundColor: '#28a745',
            color: 'white',
            textDecoration: 'none',
            borderRadius: '5px'
          }}
        >
          📜 License & Usage Terms PDF
        </a>
      </div>
    </div>
  );
};

export default AcademicDownloads;
