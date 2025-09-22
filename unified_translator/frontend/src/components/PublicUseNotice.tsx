import React from 'react';

const PublicUseNotice: React.FC = () => {
  return (
    <div style={{
      backgroundColor: '#f5f5f5',
      padding: '20px',
      borderRadius: '8px',
      marginTop: '20px'
    }}>
      <h2>🔓 Open Access for Global Research</h2>
      <p>
        The <strong>Ancient Script Universal Translator</strong> is a public tool developed by <strong>Nicolas Brett</strong> and the International Plebeian Tribunal Academy. It is designed to decode ancient scripts using the <em>Brett Method</em>—a frequency-based analytical framework grounded in harmonic resonance, archaeological context, and symbolic interpretation.
      </p>
      <p>
        This system is freely available for academic, linguistic, and cultural research. No login is required. Users may upload images or text, select a script, and receive translations, frequency breakdowns, and conceptual narratives in multiple languages.
      </p>
      <p>
        <strong>Note:</strong> All intellectual property rights to the Brett Method and its mathematical framework are retained by the creator. Commercial use, redistribution, or proprietary integration is prohibited without written consent.
      </p>
      <p>
        For licensing inquiries or collaboration proposals, contact: <a href="mailto:tribunal@plebeian.academy">tribunal@plebeian.academy</a>
      </p>
    </div>
  );
};

export default PublicUseNotice;
