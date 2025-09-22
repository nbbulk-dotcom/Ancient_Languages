import React from 'react';

const CitationGuide: React.FC = () => {
  return (
    <div style={{ 
      marginTop: '40px', 
      padding: '20px', 
      backgroundColor: '#f8f9fa', 
      borderRadius: '8px' 
    }}>
      <h2>📚 Citation Guide for Researchers</h2>
      <p>If you use this system in academic work, please cite it as follows:</p>
      <blockquote style={{ 
        backgroundColor: 'white', 
        padding: '15px', 
        borderLeft: '4px solid #007bff',
        margin: '10px 0'
      }}>
        Brett, N. (2025). "Frequency-Based Decipherment of Ancient Scripts via Symbolic Resonance." International Plebeian Tribunal Academy.<br />
        Available at: https://ancient-languages-app-pc1ray9y.devinapps.com
      </blockquote>
      <p>You may also reference the GitHub repository:</p>
      <blockquote style={{ 
        backgroundColor: 'white', 
        padding: '15px', 
        borderLeft: '4px solid #28a745',
        margin: '10px 0'
      }}>
        Brett, N. (2025). Ancient Script Universal Translator [Computer software]. GitHub.<br />
        https://github.com/nbbulk-dotcom/Ancient_Languages
      </blockquote>
      <p>For specific modules (e.g., Linear A frequency calculator, OCR subroutines), include the file name and commit hash if possible.</p>
    </div>
  );
};

export default CitationGuide;
