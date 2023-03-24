
import React, { useState } from 'react';
import IconButton from '@mui/material/IconButton';
import DeleteIcon from '@mui/icons-material/Delete';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import Box from '@mui/material/Box';

const FileInput = ({ register, obj }) => {
  const [previewSrc, setPreviewSrc] = useState(null);

  // const handleFileChange = (event) => {
  //   // deepcopy
  //   const file = {... event.target.files[0]};
  //   if (file) {
  //     const reader = new FileReader();
  //     reader.onloadend = () => {
  //       setPreviewSrc(reader.result);
  //     };
  //     reader.readAsDataURL(file);
  //   } else {
  //     setPreviewSrc(null);
  //   }
  // };

  const handleDelete = () => {
    setPreviewSrc(null);
  };

  return (
    <div style={{ marginTop: 10 }}>
      <label htmlFor={obj.name}>Upload File  </label>
      <input
        type="file"
        {...register(obj.name)}
        // onChange={handleFileChange}
        // style={{ display: 'none' }}
        id={`upload-button-${obj.name}`}
      />
      <label htmlFor={`upload-button-${obj.name}`}>
        <IconButton component="span" color="primary">
          < CloudUploadIcon fontSize='large'/>
        </IconButton>
      </label>
      <Box marginBottom={1} display='inline' >
          <IconButton onClick={handleDelete} color="secondary">
            <DeleteIcon />
          </IconButton>
          </Box>
      {previewSrc && (
        <>
          
          <img src={previewSrc} alt="Preview" style={{display:'block', maxWidth: '100%', maxHeight: '200px', marginBottom: '10px' }} />
          
        </>
      )}
    </div>
  );
};

export default FileInput;


