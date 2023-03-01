import React from 'react'

const CheckboxInput = ({register, obj}) => {
  return (
    <div style={{
        marginTop: 15
    }}>
        <label htmlFor={obj.name}>{obj.label}</label>
        <input type="checkbox" {...register("unlisted")}/>
    </div>
  )
}

export default CheckboxInput;
