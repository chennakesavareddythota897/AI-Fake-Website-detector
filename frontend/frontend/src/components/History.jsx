import React, { useState, useEffect } from 'react'
import { getHistory } from '../services/api'

const History = ({ refreshTrigger }) => {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);

  async function loadHistory() {
    setLoading(true);
    try {
      const data = await getHistory();
      setHistory(data);
    } catch (err) {
      console.error("History load failed:", err);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadHistory();
  }, [refreshTrigger]);

  return (
    <div className='history-panel'>
      <h3>Scan History</h3>
      {loading && <p>Loading...</p>}
      {!loading && history.length === 0 && <p>No scans yet.</p>}
      <ul className='history-list'>
        {history.map((item) => (
          <li key={item.id} className='history-item'>
            <span className='history-url'>{item.url}</span>
            <span className='history-status'>{item.status}</span>
            <span className='history-score'>{item.riskScore}%</span>
            <span className='history-time'>{item.scannedAt}</span>
          </li>
        ))}
      </ul>
    </div>
  )
}

export default History