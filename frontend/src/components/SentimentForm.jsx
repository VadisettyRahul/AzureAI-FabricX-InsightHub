import React, { useState } from 'react';
import axios from 'axios';

const SentimentForm = () => {
  const [text, setText] = useState('');
  const [sentiment, setSentiment] = useState(null);
  const [confidence, setConfidence] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const analyzeSentiment = async () => {
    setLoading(true);
    setError(null);
    setSentiment(null);
    setConfidence(null);

    try {
      const response = await axios.post('http://<ServiceFabricClusterIP>:8000/analyze', { text });
      setSentiment(response.data.sentiment);
      setConfidence(response.data.confidence);
    } catch (err) {
      setError('Error analyzing sentiment.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="sentiment-form">
      <h2>Sentiment Analysis</h2>
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Enter text here..."
        rows="4"
        cols="50"
      />
      <br />
      <button onClick={analyzeSentiment} disabled={loading || text.trim() === ''}>
        {loading ? 'Analyzing...' : 'Analyze Sentiment'}
      </button>
      {sentiment && (
        <div className="result">
          <h3>Result:</h3>
          <p>Sentiment: {sentiment}</p>
          <p>Confidence: {(confidence * 100).toFixed(2)}%</p>
        </div>
      )}
      {error && <p className="error">{error}</p>}
    </div>
  );
};

export default SentimentForm;
