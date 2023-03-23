import React from 'react'

const CheckboxInput = ({register, obj}) => {
  return (
    <div style={{
        marginTop: 15,marginBottom:15
    }}>
        <label htmlFor={obj.name} style={{
                    cursor: 'pointer',
                    color: '#517377',
                    fontFamily: 'Arial, sans-serif',
                    fontWeight: 'bold',
                    fontSize: '16px'
                }}> {obj.label} </label>
        <input type="checkbox" {...register(obj.name)}/>
        
    </div>
  )
}

export default CheckboxInput;
