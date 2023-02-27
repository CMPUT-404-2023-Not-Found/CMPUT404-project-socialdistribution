/*
2023-02-19
pages/Profile.js

This code is modified from a tutorial video about Authentication & Refreshing Tokens from Dennis Ivy on 2022-06-02, retrieved on 2023-02-19, to youtube.com
tutorial video here:
https://www.youtube.com/watch?v=2k8NleFjG7I
*/

import React, { useContext, useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

import AuthContext from '../context/AuthContext';

const Profile = () => {
    //  variable declarations -------------------------------------
    const [ profile, setProfile ] = useState([]);
    const [ update, setUpdate ] = useState(false);
    const { user, authTokens, logoutUser } = useContext(AuthContext);
    
    //  event listners --------------------------------------------
    useEffect(() => {
        getProfile();
    }, []);

    //  async functions -------------------------------------------
    const getProfile = async () => {
        const getProfileUrl = `http://localhost:8000/api/authors/${user.user_id}/`;
        const response = await fetch(getProfileUrl, {
            headers: {
                'Authorization': 'Bearer ' + String(authTokens.access)
            }
        });
        const data = await response.json()
        if (response.status && response.status === 200) {
            setProfile(data);
        } else if (response.statusText === 'Unauthorized'){
            logoutUser();
        } else {
            console.log('Failed to get profile');
        }
    };

    const renderProfile = (profile) => {
        if (!profile) {
            return(
                <div>No profile</div>
            );
        } else {
            return(
                <div className='profile'>
                    <div>{profile.displayName}</div>
                    <div>{profile.id}</div>
                    <div>{profile.github}</div>
                    <div>{profile.profileImage}</div>
                    <hr/>
                    <div>Full Payload: {JSON.stringify(profile)}</div>
                </div>
            );
        }
    };

    const renderUpdateForm = () => {
        
    }
    // RENDER APP =================================================
    return (
        <>
        {renderProfile(profile)}
        {update && renderUpdateForm}
        </>
    );
}

export default Profile;
