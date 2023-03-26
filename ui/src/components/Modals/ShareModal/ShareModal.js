/*
2023-03-25
ui/src/components/Modals/ShareModal/ShareModal.js

This code is modified from a video tutorial of using MUI by theatypicaldeveloper, uploaded 2022-01-09, retrieved on 2023-03-25 from youtube.com
youtube video here:
https://youtu.be/4h-VWmlfJh4
*/

import React, { useContext, useEffect, useState } from 'react';
import Box from '@mui/material/Box';
import Checkbox from '@mui/material/Checkbox';
import FormControlLabel from '@mui/material/FormControlLabel';

import AuthContext from '../../../context/AuthContext';
import BasicPagination from '../../common/BasicPagination/BasicPagination';
import Backend from '../../../utils/Backend';
import BasicModal from '../../common/BasicModal/BasicModal';
import CommonButton from '../../common/CommonButton/CommonButton';
import { getInboxUrl, isObjectEmpty, isValidHttpUrl } from '../../../utils/Utils';
import { modalStyles } from './styles';

const ShareModal = ({ open, onClose, objectNodeId }) => {
    //  variable declarations -------------------------------------
    const [ followerList, setFollowerList ] = useState([]);
    const [ sendList, setSendList ] = useState({});
    const { user, authTokens, logoutUser } = useContext(AuthContext);
    const followerEndpoint = `/api/authors/${user.user_id}/followers`;
    const itemResultsKey = 'items';

    //  event listeners -------------------------------------------
    useEffect(() => {
        if (open) {
            setSendList({});
        }
    }, [open]);

    //  functions       -------------------------------------------
    const handleChange = (e) => {
        const follower_id = e.target.value;
        const send_to_follower = e.target.checked;
        console.log(`setting ${follower_id} to ${send_to_follower}`)
        setSendList(values => ({ ...values, [follower_id]: send_to_follower}));
    }

    const handleSubmit = async (e) => {
        e.preventDefault();
        // Don't attempt send request if no followers selected
        if ( isObjectEmpty(sendList) ) { onClose(); return }
        let inboxUrls = [];
        for (const property in sendList) {
            if (sendList[property]) {
                let followerNodeId = property;
                let followerInboxUrl = getInboxUrl(followerNodeId);
                if (isValidHttpUrl(followerInboxUrl)) { 
                    inboxUrls.push(followerInboxUrl); 
                } else {
                    console.error('Not valid url for ' + followerInboxUrl)
                }
            }
        }
        // Don't attempt send request if followers selected ended up as all false
        if (inboxUrls.length <= 0 ) { onClose(); return}
        let inboxData = {
            summary: 'sharing a post',
            type: 'post',
            object: objectNodeId,
            inbox_urls: inboxUrls
        }

        console.log('Sharing inboxData: ')
        console.log(inboxData);
        
        const [ response, data ] = await Backend.post(`/api/node/object/`, authTokens.access, JSON.stringify(inboxData));
        if (response.status && response.status === 201) {
            console.log('Sent inbox data:');
            console.log(data);
        } else if (response.statusText === 'Unauthorized'){
            logoutUser();
        } else {
            console.log('Failed to send inbox data');
        }
        onClose();
    };

    // RENDER APP =================================================
    const renderCheckbox = (item) => {
        let inSendList = false;
        let isChecked = false;
        if (item.url in sendList) { inSendList = true; }
        if (inSendList) { isChecked = sendList[item.url]}
        return ( 
            <Checkbox 
                value={item.url || item.id}
                checked={isChecked}
                onChange={handleChange}
            />
        )
    }

    const renderContent = () => {
        if (!followerList || followerList.length <= 0) {
            return (
                <Box>
                    <CommonButton variant='contained' onClick={onClose}>Close</CommonButton>
                </Box>
            );
        }
        let followerListRender = [];
        followerList.forEach((item, idx) => {
            item.displayName && followerListRender.push(
                <FormControlLabel
                    key={idx} label={item.displayName ? item.displayName : item.url}
                    control={renderCheckbox(item)}
                />
            );
        });
        return (
        <form>
        <Box sx={modalStyles.inputFields}>
            {followerListRender}
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
        title={(followerList && followerList.length > 0) ? 'Share with followers?': 'Sorry, you have no followers'}
        subTitle={(followerList && followerList.length > 0) ? 'Choose who to share with' : null}
        open={open}
        onClose={onClose}
        validate={() => {}}
    >
        {open &&
            <BasicPagination 
                itemEndpoint={followerEndpoint} 
                itemResultsKey={itemResultsKey}
                setItems={(followerList) => setFollowerList(followerList)}
            />
        }
        {renderContent()}
    </BasicModal>
  );
}

export default ShareModal;
