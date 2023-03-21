// import React from 'react'

// const FileInput = ({register, obj}) => {
//   return (
//     <div style={{
//         marginTop: 15
//     }}>
      
//         <label htmlFor={obj.name} >Content: </label>
//         <input type="file" {...register(obj.name)}/>
//     </div>
//   )
// }

// export default FileInput;

// import React from 'react';
// import IconButton from '@mui/material/IconButton';
// import CloudUploadIcon from '@mui/icons-material/CloudUpload';
// import DeleteIcon from '@mui/icons-material/Delete';
// import { styled } from '@mui/system';

// const FileInputLabel = styled('label')({
//   display: 'inline-flex',
//   alignItems: 'center',
//   cursor: 'pointer',
//   padding: '8px 12px',
//   borderRadius: 4,
//   backgroundColor: '#eaeff1',
//   '&:hover': {
//     backgroundColor: '#d9d9d9',
//   },
// });

// const FileName = styled('div')({
//   marginLeft: 8,
// });

// const FileInput = ({ register, obj }) => {
//   const [file, setFile] = React.useState(null);

//   const handleFileChange = (event) => {
//     setFile(event.target.files[0]);
//   };
//   const handleRemoveFile = () => {
//     setFile(null);
//     document.getElementById(obj.name).value = '';
//   };

//   return (
//     <div style={{ marginTop: 15 }}>
//       <FileInputLabel htmlFor={obj.name}>
//         <IconButton component="span" color="primary">
//           <CloudUploadIcon fontSize='large'/>
//         </IconButton>
//         <FileName>{file ? file.name : 'Upload file'}</FileName>
//       </FileInputLabel>
//       {file && (
//         <IconButton onClick={handleRemoveFile} color="secondary" >
//           <DeleteIcon />
//         </IconButton>
//       )}
//       <input
//         type="file"
//         {...register(obj.name)}
//         id={obj.name}
//         style={{ display: 'none' }}
//         onChange={handleFileChange}
//       />
//     </div>
//   );
// };

// export default FileInput;
import React, { useState } from 'react';
import IconButton from '@mui/material/IconButton';
import DeleteIcon from '@mui/icons-material/Delete';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import Box from '@mui/material/Box';

const FileInput = ({ register, obj }) => {
  const [previewSrc, setPreviewSrc] = useState(null);

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreviewSrc(reader.result);
      };
      reader.readAsDataURL(file);
    } else {
      setPreviewSrc(null);
    }
  };

  const handleDelete = () => {
    setPreviewSrc(null);
  };

  return (
    <div style={{ marginTop: 15 }}>
      <label htmlFor={obj.name}>Upload File  </label>
      <input
        type="file"
        {...register(obj.name)}
        onChange={handleFileChange}
        style={{ display: 'none' }}
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


