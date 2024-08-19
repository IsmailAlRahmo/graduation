import React from 'react'

const TopAreas = ({tips}) => {
  return (
    <div className="w-1/2 bg-[#192533] pt-2 rounded-3xl">
          <p className="text-center">Your top areas:</p>
          <p className="text-left pl-4">{tips}</p>
        </div>
  )
}

export default TopAreas