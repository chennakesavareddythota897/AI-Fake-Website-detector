import React from 'react'

const ScanButton = ({onScan,loading}) => {
    
  return (
    <button onClick={onScan} disabled={loading} >
      {loading ? "Scanning..." : "Scan Website"}
    </button>
  )
}

export default ScanButton
