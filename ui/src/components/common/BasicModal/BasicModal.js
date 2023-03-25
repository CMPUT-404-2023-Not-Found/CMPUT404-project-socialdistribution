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
import Button from '@mui/material/Button';
import Input from '@mui/material/Input';
import Typography from '@mui/material/Typography';

import { modalStyles } from './styles';
import CommonButton from '../CommonButton/CommonButton';

const BasicModal = ({ open, onClose }) => {
    const validate = () => {

    };

    return (
        <Modal open={open} onClose={onClose}>
            <Box sx={modalStyles.wrapper}>
                <Typography variant="h6" component="h2">
                    Share with followers
                </Typography>
                <Typography sx={{ mt: 2 }}>
                    Choose which followers to share with
                </Typography>
                <Box sx={modalStyles.inputFields}>
                    <Input placeholder='this is a placeholder'></Input>
                    <Input placeholder='this is a placeholder'></Input>
                    <Input placeholder='this is a placeholder'></Input>
                </Box>
                <Box sx={modalStyles.buttons}>
                    <CommonButton variant='contained' onClick={validate}>Submit</CommonButton>
                    <CommonButton onClick={onClose}>Cancel</CommonButton>
                </Box>
            </Box>
        </Modal>
    );
}

export default BasicModal;
