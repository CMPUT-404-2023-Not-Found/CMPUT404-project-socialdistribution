
import React, { useState } from 'react';
import { TextField, IconButton, InputAdornment } from '@mui/material';
import HighlightOffIcon from '@mui/icons-material/HighlightOff';

const TextInput = ({ register, obj }) => {
  const [inputValue, setInputValue] = useState('');
  const handleDeleteClick = () => {
    setInputValue('');
  };

  const inputProps = {
    endAdornment: (
      <InputAdornment position="end">
        {inputValue && (
          <IconButton edge="end" onClick={handleDeleteClick}>
            <HighlightOffIcon />
          </IconButton>
        )}
      </InputAdornment>
    ),
  };

  if (obj.max_length && obj.max_length < 200) {
    return (
      <TextField
        label={obj.label}
        required
        {...register(obj.name)}
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
        InputProps={inputProps}
        fullWidth
        variant="outlined"
        style={{ marginBottom: 15,width:"45%" }}
        InputLabelProps={{
                style: {
                fontSize: '18px', // Set the desired font size
                fontWeight: 'bold',
            },
        }}
      />
    );
  } else {
    return (
      <TextField
        label={obj.label}
        {...register(obj.name)}
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
        InputProps={inputProps}
        fullWidth
        multiline
        rows={4}
        variant="outlined"
        style={{ marginBottom: 15 }}
        InputLabelProps={{
                style: {
                fontSize: '18px', // Set the desired font size
                fontWeight: 'bold',
            },
        }}
      />
    );
  }
};

export default TextInput;





