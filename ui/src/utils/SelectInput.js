import React from 'react'
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';

const SelectInput = ({register, obj, onChange}) => {
    return (
        <FormControl style={{ display: "block", marginTop: 15}} size="small">
            <InputLabel
            style={{ backgroundColor: '#eaeff1',fontWeight: 'bold'  }}
            htmlFor={obj.name}
            >
            {/* {obj.help_text ? obj.help_text : obj.label} */}
            {obj.label}
        </InputLabel>
          <Select  {...register(obj.name)}
          style={{ width: '15%',marginBottom:20 }}
          onChange={onChange}
          >
            <MenuItem >None</MenuItem>
            {/* <MenuItem value="">
              {obj.help_text ? obj.help_text : obj.label}
            </MenuItem> */}
            {obj.choices.map((choice, i) => (
              <MenuItem key={i} value={choice.value}>
                {choice.display_name}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
        
      )
    }
export default SelectInput
