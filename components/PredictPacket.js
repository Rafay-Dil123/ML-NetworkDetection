import { useState } from 'react';

const PredictPacket = () => {
  const [predictions, setPredictions] = useState(null);
  const [loading, setLoading] = useState(false);

  const predict = async () => {
    setLoading(true);
    const response = await fetch('/api/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ packetData: {} }), // Include packet data if needed
    });
    const data = await response.json();

    if (data.success) {
      setPredictions(data.predictions);
    } else {
      setPredictions('Prediction failed. Check logs.');
    }
    setLoading(false);
  };

  return (
    <div>
      <h1>Predict Network Packet</h1>
      <button onClick={predict} disabled={loading}>
        {loading ? 'Predicting...' : 'Start Prediction'}
      </button>
      {predictions && (
        <div>
          <h2>Prediction Results</h2>
          <pre>{predictions}</pre>
        </div>
      )}
    </div>
  );
};

export default PredictPacket;
