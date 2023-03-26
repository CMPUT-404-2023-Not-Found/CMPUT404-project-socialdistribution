/*
2023-03-24
ui/src/components/common/BasicModal/BasicModal.js

This code is modified from a video tutorial of using MUI by theatypicaldeveloper, uploaded 2022-01-09, retrieved on 2023-03-25 from youtube.com
youtube video here:
https://youtu.be/4h-VWmlfJh4
*/

import React from 'react';
import Box from '@mui/material/Box';
import Modal from '@mui/material/Modal';
import Typography from '@mui/material/Typography';

import { modalStyles } from './styles';

const BasicModal = ({ title, subTitle, content, open, onClose }) => {

    return (
        <Modal aria-labelledby={title} aria-describedby={subTitle} open={open} onClose={onClose}>
            <Box sx={modalStyles.wrapper}>
                <Typography id={title} variant="h6" component="h2">
                    {title}
                </Typography>
                <Typography id={subTitle} sx={{ mt: 2 }}>
                    {subTitle}
                </Typography>
                {content}
            </Box>
        </Modal>
    );
}

export default BasicModal;
