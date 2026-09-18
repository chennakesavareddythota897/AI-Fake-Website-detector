import React from 'react'

const FEATURE_LABELS = {
  is_https: "HTTPS Enabled",
  is_trusted: "Trusted Domain",
  is_ip_domain: "Uses IP Address",
  url_length: "URL Length",
  keyword_count: "Suspicious Keywords",
  subdomain_count: "Subdomain Count",
  hyphen_count: "Hyphen Count",
  digit_ratio: "Digit Ratio in Domain",
  at_symbol: "Contains '@' Symbol",
}

const BOOLEAN_FEATURES = ["is_https", "is_trusted", "is_ip_domain", "at_symbol"]

const ThreatReport = ({ details, riskScore, scannedUrl }) => {
  if (!details) return null;

  return (
    <div className='threat-report'>
      <h3>Threat Analysis Report</h3>
      <p className='report-subtitle'>Detailed breakdown for: <span title={scannedUrl}>{scannedUrl}</span></p>

      <div className='confidence-bar-wrapper'>
        <div className='confidence-label'>
          <span>AI Confidence (Phishing Probability)</span>
          <span>{riskScore}%</span>
        </div>
        <div className='confidence-bar-track'>
          <div
            className='confidence-bar-fill'
            style={{
              width: `${riskScore}%`,
              backgroundColor: riskScore > 70 ? '#dc2626' : riskScore > 30 ? '#f59e0b' : '#16a34a',
            }}
          />
        </div>
      </div>

      <table className='feature-table'>
        <tbody>
          {Object.entries(details).map(([key, value]) => (
            <tr key={key}>
              <td>{FEATURE_LABELS[key] || key}</td>
              <td className={BOOLEAN_FEATURES.includes(key) ? (value ? 'flag-bad' : 'flag-good') : ''}>
                {BOOLEAN_FEATURES.includes(key)
                  ? (value ? "Yes" : "No")
                  : (typeof value === "number" ? value.toFixed(2).replace(/\.00$/, "") : value)}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default ThreatReport