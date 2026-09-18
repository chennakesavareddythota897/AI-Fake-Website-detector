import React from 'react'

const WarningBanner = ({ riskScore }) => {
  if (riskScore <= 70) return null;

  return (
    <div className='warning-banner'>
      <span className='warning-icon'>🚨</span>
      <div>
        <h2>DANGER: Phishing Site Detected!</h2>
        <p>This website has been flagged as unsafe. Do not enter personal information such as passwords or card details.</p>
      </div>
    </div>
  )
}

export default WarningBanner