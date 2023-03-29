/*
2023-03-22
pages/Followers/Followers.js
*/
import React, { useContext, useEffect, useState } from 'react';
import Alert from '@mui/material/Alert';
import { Typography, IconButton } from '@mui/material';
import PersonRemoveIcon from '@mui/icons-material/PersonRemove';
import Snackbar from '@mui/material/Snackbar';

import AuthContext from '../../context/AuthContext';
import AuthorCard from '../../components/Author/AuthorCard';
import BasicCard from '../../components/common/BasicCard/BasicCard';
import Backend from '../../utils/Backend';
import GridWrapper from '../../components/common/GridWrapper/GridWrapper';
import PageHeader from '../../components/Page/PageHeader';
import SearchBar from '../../components/SearchBar/SearchBar';
import { isValidHttpUrl, getInboxUrl } from '../../utils/Utils'

const Followers = () => {
    //  variable declarations -------------------------------------
    const [ showNotification, setShowNotification ] = React.useState(false);
    const [ notificationSeverity, setNotificationSeverity ] = useState('info');
    const [ notificationMessage, setNotificationMessage ] = useState('');

    const [ followers, setFollowers ] = useState([]);
    const { user, authTokens, logoutUser } = useContext(AuthContext);
    const [ input, setInput ] = useState('');

    //  event listeners --------------------------------------------
    useEffect(() => {
        const getFollowers = async () => {
            const [response, data] = await Backend.get(`/api/authors/${user.user_id}/followers/`, authTokens.access);
            if (response.status && response.status === 200) {
                console.log('Got followers list ...');
                console.debug(data);
                setFollowers(data.items);
            } else if (response.statusText === 'Unauthorized'){
                logoutUser();
            } else {
                console.error('Failed to get followers');
            }
        };
        getFollowers();
    }, [ user, authTokens, logoutUser ]);

    const deleteFollower = async (follower, idx) => {
        console.info('Deleting follower ...');
        const follower_id = follower.id || follower.object;
        console.debug(follower_id);
        const response = await Backend.delete(`/api/authors/${user.user_id}/followers/${follower_id}/`, authTokens.access);
        if (response.status && response.status === 204) {
            console.log("Deleted follower " + follower_id);
            followers.splice(idx,1);
            setFollowers([...followers]);
            setNotificationMessage('Deleted follower ' + follower_id);
            setShowNotification(true);
            setNotificationSeverity('success');
        } else if (response.statusText === 'Unauthorized'){
            logoutUser();
        } else {
            console.error('Failed to delete follower');
            setNotificationMessage('Failed to delete follower ' + follower_id);
            setShowNotification(true);
            setNotificationSeverity('error');
        }
    }
    
    // This is where we POST to the "object's" inbox
    const sendFollowRequest = async () => {
        console.log('Attemtping follower request ...')
        console.debug(input);
        if (!isValidHttpUrl(input)){
            setNotificationMessage('Invalid follower id');
            setShowNotification(true);
            setNotificationSeverity('error');
            setInput('');
            return
        }
        let profile;
        const [response, data] = await Backend.get(`/api/authors/${user.user_id}/`, authTokens.access);
        if (response.status && response.status === 200) {
            console.log("Got profile ...");
            console.debug(data);
            profile = data;
        } else if (response.statusText === 'Unauthorized'){
            logoutUser();
        } else {
            console.error('Failed to get profile');
        }
        console.log('Sending follower request inbox data ...')
        console.debug(input);
        let inboxData = {
            summary: 'I want to follow you',
            type: 'Follow',
            object: {
                url: input
            },
            inbox_urls : [getInboxUrl(input)]
        }
        const [ frResponse, frData ] = await Backend.post(`/api/node/object/`, authTokens.access, JSON.stringify(inboxData));
        if (frResponse.status && frResponse.status === 201) {
            setNotificationMessage('Follow request sent!');
            setNotificationSeverity('success');
            setShowNotification(true);
        } else if (frResponse.statusText === 'Unauthorized'){
            logoutUser();
        } else {
            console.log('Failed to send request');
            console.debug(frResponse);
        }
        setInput('');
    }

    const handleChange = (event) => {
        setInput(event.target.value);
    }

    const handleClose = (event, reason) => {
        if (reason === 'clickaway') {
            return;
        }
        setShowNotification(false);
    };

    // render functions ------------------------------------------
    const renderSearchBar = () => {
        return (
            <>
            <BasicCard 
                content = {<SearchBar 
                    placeholder='Enter Author ID'
                    value={input}
                    onChange={(event) => handleChange(event)}
                    onSearch={() => sendFollowRequest()}
                />}
            />
            </>
        )
    }
    const renderFollowers = (followers) => {
        if (!followers || followers.length <= 0) return (<Typography paragraph >No Followers</Typography>);
        let itemsRender = [];
        followers.forEach((follower, idx) => {
            itemsRender.push(
                <AuthorCard author = {follower} size = "medium"> 
                    <div>
                        <IconButton 
                            aria-label="delete-follower"
                            onClick={()=> deleteFollower(follower, idx)}>
                        <PersonRemoveIcon/>
                        </IconButton>
                    </div>
                </AuthorCard>
            );
            itemsRender.push(<br key={idx + followers.length}></br>);
        });
        return (<>{itemsRender}</>);
    }
    // RENDER APP =================================================
    return (
    <>
        <PageHeader followers={followers} title='Followers'></PageHeader>
        <GridWrapper>
            {renderSearchBar()}
            {renderFollowers(followers)}
            <Snackbar
                open={showNotification}
                autoHideDuration={6000}
                onClose={handleClose}
            >
                <Alert onClose={handleClose} severity={notificationSeverity} sx={{ width: '100%' }}>
                    {notificationMessage}
                </Alert>
            </Snackbar>
        </GridWrapper>
    </>
  )
}

export default Followers
