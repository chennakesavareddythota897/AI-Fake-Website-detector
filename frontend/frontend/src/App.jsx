import {useState,useEffect}from 'react'
import Header from "./components/Header.jsx";
import StatusCard from "./components/StatusCard.jsx";
import ScanButton from "./components/ScanButton.jsx";
import ResultCard from './components/ResultCard.jsx';
import {scanWebsite} from "./services/api"
const App = () => {
  const [status, setStatus] = useState("⚪ Not Scanned");
  const [riskScore,setRiskScore] = useState(0);
  const [loading,setLoading] = useState(false);
  const [reasons,setReasons] = useState([]);

  async function handleScan() {

    setLoading(true);
  setStatus("🔄 Scanning...");
const result = await scanWebsite();
console.log(result)
setStatus(result.status);
setRiskScore(result.riskScore);
setReasons(result.reasons)
setLoading(false);
  }
  
  useEffect(()=>{
    console.log("Status changed:",status  );
  },[status])
  return (
    <div>
   
     <Header/>    
     <StatusCard
     website="https://google.com"
     status={status}
     />
     <ScanButton onScan={handleScan} loading={loading} />
     <ResultCard riskScore={riskScore} reasons={reasons} /> 
    </div>
  )
}

export default App
