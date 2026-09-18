import { useState, useEffect } from 'react'
import Header from "./components/Header.jsx";
import StatusCard from "./components/StatusCard.jsx";
import ScanButton from "./components/ScanButton.jsx";
import ResultCard from './components/ResultCard.jsx';
import { scanWebsite } from "./services/api"
import WarningBanner from "./components/WarningBanner.jsx";
import History from "./components/History.jsx";
import ThreatReport from "./components/ThreatReport.jsx";

const App = () => {
  const [url, setUrl] = useState("https://google.com");
  const [status, setStatus] = useState("⚪ Not Scanned");
  const [riskScore, setRiskScore] = useState(0);
  const [loading, setLoading] = useState(false);
  const [reasons, setReasons] = useState([]);
  const [error, setError] = useState("");
  const [historyRefresh, setHistoryRefresh] = useState(0);
  const [details, setDetails] = useState(null);

  useEffect(() => {
    if (typeof chrome !== "undefined" && chrome.tabs) {
      chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        if (tabs[0]?.url) {
          setUrl(tabs[0].url);
        }
      });
    }
  }, []);

  async function handleScan() {
    if (!url.trim()) {
      setError("Please enter a URL to scan");
      return;
    }
    setError("");
    setLoading(true);
    setStatus("🔄 Scanning...");
    try {
      const result = await scanWebsite(url);
      setStatus(result.status);
      setRiskScore(result.riskScore);
      setReasons(result.reasons);
      setDetails(result.details);
      setHistoryRefresh(prev => prev + 1);
    } catch (err) {
      console.error(err);
      setError("Could not connect to backend. Please check if the server is running.");
      setStatus("⚪ Not Scanned");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <Header />
      <WarningBanner riskScore={riskScore} />
      <div style={{ padding: "16px" }}>
        <input
          type="text"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="https://example.com"
          style={{ width: "300px", padding: "8px", marginRight: "8px" }}
        />
      </div>
      {error && <p style={{ color: "red", padding: "0 16px" }}>{error}</p>}
      <StatusCard website={url} status={status} />
      <ScanButton onScan={handleScan} loading={loading} />
      <ResultCard riskScore={riskScore} reasons={reasons} />
      <ThreatReport details={details} riskScore={riskScore} scannedUrl={url} />
      <History refreshTrigger={historyRefresh} />
    </div>
  )
}

export default App