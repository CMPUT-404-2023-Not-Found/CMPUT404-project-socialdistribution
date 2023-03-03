import React from 'react'

const SelectInput = ({register, obj}) => {
  return (
    <select {...register(obj.name)} style={{
        display: 'block',
        marginTop: 15
    }}>
    {
        obj.help_text ? 
            <option value="">-- {obj.help_text} --</option>
        :   <option value="">-- {obj.label} --</option>
    }

    {
        obj.choices.map((choice, i) => {
            return (
                <option key={i} value={choice.value}>{choice.display_name}</option>
            )
        })
    }
    </select>
  )
}

export default SelectInput
