import React from 'react'

const ResultCard = ({riskScore,reasons}) => {
  let color = "green";
  if (riskScore > 70){
    color = "red";
  } else if (riskScore > 30){
    color = "orange";
  }
  return (
    <div className='result-card'>
    <h3>Scan Result</h3>
    <p style={{ color:color}}>Risk Score: {riskScore}%</p>
    <p>Reason:</p>
    <ul>
       {reasons.map((reason, index)=>(
        <li key={index}>{reason}</li>
       ))}
        </ul>      
    </div>
  )
}

export default ResultCard
