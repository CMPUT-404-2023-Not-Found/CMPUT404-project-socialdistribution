import { color } from '@mui/system';
import React from 'react'
import { useState } from 'react';
import HighlightOffIcon from '@mui/icons-material/HighlightOff';


const TextInput = ({register, obj}) => {
    
        const [inputValue, setInputValue] = useState('');
        const handleDeleteClick = () => {
          setInputValue('');
        };
      
        if (obj.max_length && obj.max_length < 200) {
          return (
            <>
              <label htmlFor={obj.name}>{obj.label} </label>
              <div style={{ display: 'flex', alignItems: 'center' }}>
                <input
                  {...register(obj.name)}
                  style={{
                    display: 'block',
                    marginBottom: 15,
                    height: 30,
                  }}
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                />
                {inputValue && (
                  <HighlightOffIcon
                    style={{ cursor: 'pointer' , marginLeft:-25,marginBottom:15,backgroundColor:'white',color:'#517377'}}
                    onClick={handleDeleteClick}
                  />
                )}
              </div>
              
            </>
          );
        } 
        else {
            return (
                <>
                  <label htmlFor={obj.name}>{obj.label}</label>
                  <div style={{ display: 'flex', alignItems: 'center' }}>
                    <textarea
                      {...register(obj.name)}
                      style={{
                        display: 'block',
                        verticalAlign: 'top',
                        marginBottom: 15,
                      }}
                      value={inputValue}
                      onChange={(e) => setInputValue(e.target.value)}
                    />
                    {inputValue && (
                      <HighlightOffIcon
                        style={{ cursor: 'pointer', marginLeft: -25, marginBottom: 15, backgroundColor: 'white', color: '#517377' }}
                        onClick={handleDeleteClick}
                      />
                    )}
                  </div>
                </>
              );
            }
          };

export default TextInput;





