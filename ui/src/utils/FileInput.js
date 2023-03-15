import React from 'react'

const FileInput = ({register, obj}) => {
  return (
    <div style={{
        marginTop: 15
    }}>
        <label htmlFor={obj.name}>{obj.label}</label>
        <input type="file" {...register(obj.name)}/>
    </div>
  )
}

export default FileInput;
