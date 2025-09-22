import React, { useState } from 'react';
import './App.css';
import PublicUseNotice from './src/components/PublicUseNotice';
import AcademicDownloads from './src/components/AcademicDownloads';
import CitationGuide from './src/components/CitationGuide';

interface OCRResult {
  extracted_text: string;
  confidence?: number;
  processing_method?: string;
}

interface FrequencyResult {
  frequency_vector: Array<{glyph: string, frequency: number}>;
  harmonic_analysis?: {
    harmonic_mean: number;
    adjusted_mean: number;
    cultural_modifier: number;
    spiritual_context: string;
  };
  brett_method_validation?: boolean;
}

interface NarrativeResult {
  narrative: string;
  cultural_context?: string;
  glyph_count?: number;
  methodology?: string;
  confidence_level?: number;
}

function App() {
  const [image, setImage] = useState<File | null>(null);
  const [scriptType, setScriptType] = useState('linear_a');
  const [context, setContext] = useState('ceremonial');
  const [targetLanguage, setTargetLanguage] = useState('English');
  
  const [ocrResult, setOcrResult] = useState<OCRResult | null>(null);
  const [frequencyResult, setFrequencyResult] = useState<FrequencyResult | null>(null);
  const [narrativeResult, setNarrativeResult] = useState<NarrativeResult | null>(null);
  
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleImageUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setImage(file);
      setOcrResult(null);
      setFrequencyResult(null);
      setNarrativeResult(null);
      setError(null);
    }
  };

  const handleOCR = async () => {
    if (!image) {
      setError('Please select an image first');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append('file', image);
      formData.append('script_type', scriptType);

      const response = await fetch('/ocr', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`OCR failed: ${response.statusText}`);
      }

      const result: OCRResult = await response.json();
      setOcrResult(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'OCR processing failed');
    } finally {
      setLoading(false);
    }
  };

  const handleFrequencyAnalysis = async () => {
    if (!ocrResult) {
      setError('Please extract text first');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append('text', ocrResult.extracted_text);
      formData.append('script', scriptType);

      const response = await fetch('/translate', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Frequency analysis failed: ${response.statusText}`);
      }

      const result: FrequencyResult = await response.json();
      setFrequencyResult(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Frequency analysis failed');
    } finally {
      setLoading(false);
    }
  };

  const handleNarrativeGeneration = async () => {
    if (!ocrResult) {
      setError('Please extract text first');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append('text', ocrResult.extracted_text);
      formData.append('context', context);

      const response = await fetch('/narrative', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Narrative generation failed: ${response.statusText}`);
      }

      const result: NarrativeResult = await response.json();
      setNarrativeResult(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Narrative generation failed');
    } finally {
      setLoading(false);
    }
  };

  const handleFullTranslation = async () => {
    await handleOCR();
    setTimeout(async () => {
      await handleFrequencyAnalysis();
      setTimeout(async () => {
        await handleNarrativeGeneration();
      }, 1000);
    }, 1000);
  };

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <PublicUseNotice />

      <div style={{ marginTop: '30px' }}>
        <h1>🏺 Ancient Script Universal Translator</h1>
        <p><em>Powered by The Brett Method - Unified MANUS & GROK System</em></p>
        
        <div style={{ marginBottom: '20px' }}>
          <label>Upload Ancient Script Image:</label><br />
          <input 
            type="file" 
            accept="image/*"
            onChange={handleImageUpload} 
            style={{ marginTop: '5px' }}
          />
        </div>

        <div style={{ marginBottom: '20px' }}>
          <label>Script Type: </label>
          <select 
            value={scriptType} 
            onChange={(e) => setScriptType(e.target.value)}
            style={{ marginLeft: '10px', marginRight: '20px' }}
          >
            <option value="linear_a">Linear A (Minoan)</option>
            <option value="khitan">Khitan Large Script</option>
            <option value="proto_elamite">Proto-Elamite</option>
            <option value="indus_valley">Indus Valley Script</option>
          </select>

          <label>Context: </label>
          <select 
            value={context} 
            onChange={(e) => setContext(e.target.value)}
            style={{ marginLeft: '10px', marginRight: '20px' }}
          >
            <option value="ceremonial">Ceremonial</option>
            <option value="administrative">Administrative</option>
            <option value="religious">Religious</option>
            <option value="imperial">Imperial</option>
            <option value="vedic">Vedic</option>
            <option value="economic">Economic</option>
          </select>

          <label>Language: </label>
          <select 
            value={targetLanguage} 
            onChange={(e) => setTargetLanguage(e.target.value)}
            style={{ marginLeft: '10px' }}
          >
            <option value="English">English</option>
            <option value="Spanish">Español</option>
            <option value="French">Français</option>
            <option value="German">Deutsch</option>
            <option value="Italian">Italiano</option>
            <option value="Portuguese">Português</option>
            <option value="Chinese">中文</option>
            <option value="Japanese">日本語</option>
          </select>
        </div>
        
        <div className="button-group">
          <button 
            onClick={handleOCR}
            disabled={!image || loading}
            className="action-button primary"
          >
            🔍 Convert Image to Characters
          </button>
          <button 
            onClick={handleFrequencyAnalysis}
            disabled={!ocrResult || loading}
            className="action-button secondary"
          >
            📊 Analyze Frequency
          </button>
          <button 
            onClick={handleNarrativeGeneration}
            disabled={!ocrResult || loading}
            className="action-button secondary"
          >
            📜 Generate Narrative
          </button>
          <button 
            onClick={handleFullTranslation}
            disabled={!image || loading}
            className="action-button full-translation"
          >
            🏺 Complete Translation Pipeline
          </button></div>
        
        {loading && (
          <div className="loading-indicator">
            <div className="spinner"></div>
            <p>⏳ Processing ancient script using Brett Method...</p>
          </div>
        )}

        {error && (
          <div style={{ 
            backgroundColor: '#f8d7da', 
            padding: '15px', 
            borderRadius: '5px', 
            marginBottom: '20px',
            color: '#721c24'
          }}>
            <p>❌ {error}</p>
          </div>
        )}

        {image && (
          <div style={{ 
            backgroundColor: '#e9ecef', 
            padding: '15px', 
            borderRadius: '5px', 
            marginBottom: '20px' 
          }}>
            <h3>📸 Selected Image:</h3>
            <img 
              src={URL.createObjectURL(image)} 
              alt="Selected ancient script" 
              style={{ maxWidth: '400px', maxHeight: '300px' }}
            />
          </div>
        )}

        <div className="results-section">
          {ocrResult && (
            <div className="result-card">
              <h3>🔤 Extracted Glyphs & Symbols</h3>
              <div className="glyph-display">
                {ocrResult.extracted_text.split(' ').map((glyph, index) => (
                  <div key={index} className="glyph-item">
                    {glyph}
                    <small>Glyph {index + 1}</small>
                  </div>
                ))}
              </div>
              <div className="processing-method">
                Processing Method: {ocrResult.processing_method || 'Enhanced GROK OCR'}
                {ocrResult.confidence && (
                  <span> | Confidence: {(ocrResult.confidence * 100).toFixed(1)}%</span>
                )}
              </div>
            </div>
          )}

          {frequencyResult && (
            <div className="result-card">
              <h3>📊 Brett Method Frequency Analysis</h3>
              <div className="frequency-breakdown">
                {frequencyResult.frequency_vector.map((item, index) => (
                  <div key={index} className="frequency-item">
                    <span className="glyph">{item.glyph}</span>
                    <span className="frequency">{item.frequency.toFixed(2)} Hz</span>
                  </div>
                ))}
              </div>
              {frequencyResult.harmonic_analysis && (
                <div className="harmonic-analysis">
                  <h4>🎵 Harmonic Analysis</h4>
                  <p>Harmonic Mean: {frequencyResult.harmonic_analysis.harmonic_mean} Hz</p>
                  <p>Adjusted Mean: {frequencyResult.harmonic_analysis.adjusted_mean} Hz</p>
                  <p>Cultural Modifier: {frequencyResult.harmonic_analysis.cultural_modifier}x</p>
                  <p>Spiritual Context: {frequencyResult.harmonic_analysis.spiritual_context}</p>
                </div>
              )}
            </div>
          )}

          {narrativeResult && (
            <div className="result-card">
              <h3>📖 Cultural Narrative Interpretation</h3>
              <div className="narrative-content">
                <div className="narrative-text">{narrativeResult.narrative}</div>
                <div className="narrative-metadata">
                  <p><strong>Cultural Context:</strong> {narrativeResult.cultural_context}</p>
                  <p><strong>Methodology:</strong> {narrativeResult.methodology}</p>
                  <p><strong>Confidence Level:</strong> {narrativeResult.confidence_level && (narrativeResult.confidence_level * 100).toFixed(1)}%</p>
                </div>
              </div>
            </div>
          )}
        </div>

        <AcademicDownloads />
        <CitationGuide />
      </div>
    </div>
  );
}

export default App;
