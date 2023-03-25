/*
2023-03-24
ui/src/components/common/BasicModal/BasicModal.js

*/

import React from 'react';
import Box from '@mui/material/Box';
import Modal from '@mui/material/Modal';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';

const BasicModal = ({ open, onClose }) => {
    const style = {
        position: 'absolute',
        top: '50%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
        width: 400,
        bgcolor: 'background.paper',
        border: '2px solid #000',
        boxShadow: 24,
        p: 4,
      };
    return (
        <Modal open={open} onClose={onClose}>
            <Box sx={style}>
                <Typography id="spring-modal-title" variant="h6" component="h2">
                Text in a modal
                </Typography>
                <Typography id="spring-modal-description" sx={{ mt: 2 }}>
                Duis mollis, est non commodo luctus, nisi erat porttitor ligula.
                </Typography>
            </Box>
        </Modal>
    );
}

export default BasicModal;
