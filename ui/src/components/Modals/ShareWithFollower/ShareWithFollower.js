/*
2023-03-25
ui/src/components/Modals/ShareWithFollower/ShareWithFollower.js

This code is modified from a video tutorial of using MUI by theatypicaldeveloper, uploaded 2022-01-09, retrieved on 2023-03-25 from youtube.com
youtube video here:
https://youtu.be/4h-VWmlfJh4
*/

import React from 'react';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Input from '@mui/material/Input';

import BasicModal from '../../common/BasicModal/BasicModal';
import { modalStyles } from './styles';

const ShareWithFollower = ({ open, onClose }) => {
    const renderContent = () => {
        return (
        <Box sx={modalStyles.inputFields}>
            <Input placeholder='Follower 1'></Input>
            <Input placeholder='Follower 2'></Input>
            <Input placeholder='Follower 3'></Input>
        </Box>
        );
    };

    return (
    <BasicModal
        title='Share with followers?' 
        subTitle='Choose which followers to share with' 
        open={open}
        onClose={onClose}
        content={renderContent()}
        validate={() => {}}
    >
        ShareWithFollower
    </BasicModal>
  );
}

export default ShareWithFollower;
