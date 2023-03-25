/*
2023-03-25
ui/src/components/Modals/ShareWithFollower/ShareWithFollower.js

This code is modified from a video tutorial of using MUI by theatypicaldeveloper, uploaded 2022-01-09, retrieved on 2023-03-25 from youtube.com
youtube video here:
https://youtu.be/4h-VWmlfJh4
*/

import React, { useEffect, useState } from 'react';
import Box from '@mui/material/Box';
import Checkbox from '@mui/material/Checkbox';
import FormControlLabel from '@mui/material/FormControlLabel';

import BasicModal from '../../common/BasicModal/BasicModal';
import CommonButton from '../../common/CommonButton/CommonButton';
import { modalStyles } from './styles';

const ShareWithFollower = ({ open, onClose }) => {
    const [ followerList, setFollowerList ] = useState([]);
    const [ sendList, setSendList ] = useState({});
    
    const handleChange = (e) => {
        const follower_id = e.target.value;
        const send_to_follower = e.target.checked;
        setSendList(values => ({ ...values, [follower_id]: send_to_follower}));
    }
    const handleSubmit = (e) => {
        e.preventDefault();
        console.log('xxx submit! sending to: ');
        console.log(sendList);
        onClose();
    };

    useEffect(() => {
      if (open) setSendList({});
    }, [open]);
    

    const renderContent = () => {
        return (
        <form>
        <Box sx={modalStyles.inputFields}>
            <FormControlLabel label='follower 1' control={<Checkbox value='follower_1' onChange={handleChange}/>} />
            <FormControlLabel label='follower 2' control={<Checkbox value='follower_2' onChange={handleChange}/>} />
            <FormControlLabel label='follower 3' control={<Checkbox value='follower_3' onChange={handleChange}/>} />
        </Box>
        <Box sx={modalStyles.buttons}>
            <CommonButton variant='contained' onClick={handleSubmit}>Submit</CommonButton>
            <CommonButton onClick={onClose}>Cancel</CommonButton>
        </Box>
        </form>
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
