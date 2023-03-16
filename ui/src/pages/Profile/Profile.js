/*
2023-02-19
pages/Profile.js

This code is modified from a tutorial video about Authentication & Refreshing Tokens from Dennis Ivy on 2022-06-02, retrieved on 2023-02-19, to youtube.com
tutorial video here:
https://www.youtube.com/watch?v=2k8NleFjG7I
*/

import React, { useContext, useEffect, useState } from 'react';
import { CardContent, CardHeader, IconButton, Typography } from '@mui/material';
import GitHubIcon from '@mui/icons-material/GitHub';
import ToolTip from '@mui/material/Tooltip';

import BasicAvatar from '../../components/common/BasicAvatar/BasicAvatar';
import BasicCard from '../../components/common/BasicCard/BasicCard';
import GridWrapper from '../../components/common/GridWrapper/GridWrapper';
import AuthContext from '../../context/AuthContext';
import Backend from '../../utils/Backend';

const Profile = () => {
    //  variable declarations -------------------------------------
    const [ displayName, setDisplayName ] = useState('');
    const [ profile, setProfile ] = useState({});
    const [ update, setUpdate ] = useState(false);
    const { user, authTokens, logoutUser } = useContext(AuthContext);
    
    //  event listners --------------------------------------------
    useEffect(() => {
        const getProfile = async () => {
            const [response, data] = await Backend.get(`/api/authors/${user.user_id}/`, authTokens.access);
            if (response.status && response.status === 200) {
                console.log('Got profile');
                console.log(data);
                setProfile(data);
            } else if (response.statusText === 'Unauthorized'){
                logoutUser();
            } else {
                console.log('Failed to get profile');
            }
        };
        getProfile();
    }, [ user, authTokens, logoutUser ]);

    //  async functions -------------------------------------------

    const updateProfile = async (e) => {
        e.preventDefault();
        const postData = JSON.stringify({
            displayName: displayName
        })
        const [response, responseData] = await Backend.post(`/api/authors/${user.user_id}/`, authTokens.access, postData);
        if (response.status && response.status === 200) {
            setProfile(responseData);
            setDisplayName('');
            setUpdate(false);
        } else {
            console.log('Failed to post profile');
        }
    };

    // render functions ------------------------------------------
    const renderProfile = () => {
        if (!profile) {
            return (
                <BasicCard>
                    <CardHeader title='Opps' subheader="Couldn't Find Profile"></CardHeader>
                    <CardContent></CardContent>
                </BasicCard>
            )
        }
        let profileTitle = (profile.displayName ? profile.displayName : user.username)
        return (
            <BasicCard>
                <CardHeader
                    avatar={
                        <BasicAvatar profile={profile} size='large'></BasicAvatar>
                    }
                    title={profileTitle}
                    titleTypographyProps={{ variant: 'h3' }}
                    subheader={profile.host}
                    subheaderTypographyProps={{ variant: 'h4' }}
                    action={
                    <ToolTip title={(profile.github && profile.github)}>
                    <IconButton size='large' aria-label="github" onClick={() => { console.log(profile.github) }}>
                        <GitHubIcon fontSize='large'/>
                    </IconButton>
                    </ToolTip>
                    }
                />
                <CardContent>
                    <Typography variant='h5'>ID</Typography>
                    <Typography variant='body1'>{profile.url}</Typography>
                </CardContent>
            </BasicCard>
        )
    }

    const renderUpdateForm = () => {
        if (!update) {
            return (
                <div>
                    <button onClick={() => setUpdate(true)}>Update Account</button>
                </div>
            )
        } else {
            return (
                <div>
                    <form onSubmit={updateProfile}>
                        <fieldset>
                            <label htmlFor="username">Display Name </label>
                            <input 
                                type="text" 
                                id="username" 
                                name="username" 
                                placeholder="Type your username" 
                                onChange={(e) => setDisplayName(e.target.value)}
                                />
                            <br></br>
                            <br></br>
                            <input type="submit" value="Update"/>
                            <button onClick={() => setUpdate(false)}>Cancel</button>
                            <br></br>
                        </fieldset>
                    </form>
                </div>
            )
        }


    }
    // RENDER APP =================================================
    return (
        <GridWrapper>
        {renderProfile()}
        {renderUpdateForm()}
        </GridWrapper>
    );
}

export default Profile;
