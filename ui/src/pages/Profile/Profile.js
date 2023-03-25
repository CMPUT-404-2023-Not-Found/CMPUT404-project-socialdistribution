/*
2023-02-19
pages/Profile.js

This code is modified from a tutorial video about Authentication & Refreshing Tokens from Dennis Ivy on 2022-06-02, retrieved on 2023-02-19, to youtube.com
tutorial video here:
https://www.youtube.com/watch?v=2k8NleFjG7I
*/

import React, { useContext, useEffect, useState } from 'react';
import { CardContent, CardHeader } from '@mui/material';

import BasicCard from '../../components/common/BasicCard/BasicCard';
import GridWrapper from '../../components/common/GridWrapper/GridWrapper';
import AuthContext from '../../context/AuthContext';
import Backend from '../../utils/Backend';
import PageHeader from '../../components/Page/PageHeader';
import AuthorCard from '../../components/Author/AuthorCard';

const Profile = () => {
    //  variable declarations -------------------------------------
    const [ displayName, setDisplayName ] = useState('');
    const [ profile, setProfile ] = useState({});
    const [ update, setUpdate ] = useState(false);
    const { user, authTokens, logoutUser } = useContext(AuthContext);
    
    //  event listeners --------------------------------------------
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
                    <CardHeader title='Oops' subheader="Couldn't Find Profile"></CardHeader>
                    <CardContent></CardContent>
                </BasicCard>
            )
        }
        // let profileTitle = (profile.displayName ? profile.displayName : user.username)
        return (
            <AuthorCard
                author = {profile} 
                size = "large" 
            />
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
        <>
            <PageHeader profile={profile} title='Profile'></PageHeader>
            <GridWrapper>
                {renderProfile()}
                {renderUpdateForm()}
            </GridWrapper>
        </>
    );
}

export default Profile;
