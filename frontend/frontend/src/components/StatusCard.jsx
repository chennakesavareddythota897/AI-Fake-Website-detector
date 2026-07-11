import React from 'react'

const StatusCard = ({website,status}) => {
  return (
    <div className='status-card'>
        <h3> Current Website</h3>
        <p>{website}</p>
      <h3> Status</h3>
      <p>{status}</p>
    </div>
  )
}

export default StatusCard
