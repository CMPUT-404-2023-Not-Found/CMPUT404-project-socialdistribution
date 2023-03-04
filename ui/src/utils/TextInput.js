import React from 'react'

const TextInput = ({register, obj}) => {
    if (obj.max_length) {
        return (
            <>
                <label htmlFor={obj.name}>{obj.label}</label>
                <input {...register(obj.name)} style={{
                    display: 'block',
                    marginBottom: 15
                }}/>
            </>
        )
    } else {
        return (
            <>
                <label htmlFor={obj.name}>{obj.label}</label>
                <textarea {...register(obj.name)} style={{
                    display: 'block',
                    verticalAlign: 'top',
                    marginBottom: 15
                }}/>
            </>
        )
    }

}

export default TextInput;
