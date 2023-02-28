/*
2023-02-19
pages/Profile.js

This code is modified from a tutorial video about Authentication & Refreshing Tokens from Dennis Ivy on 2022-06-02, retrieved on 2023-02-19, to youtube.com
tutorial video here:
https://www.youtube.com/watch?v=2k8NleFjG7I
*/

import React, { useContext, useEffect, useState } from 'react';

import AuthContext from '../context/AuthContext';
import Backend from '../utils/Backend';

const Profile = () => {
    //  variable declarations -------------------------------------
    const [ profile, setProfile ] = useState([]);
    const [ update, setUpdate ] = useState(false);
    const { user, authTokens, logoutUser } = useContext(AuthContext);
    
    //  event listners --------------------------------------------
    useEffect(() => {
        getProfile();
    // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    //  async functions -------------------------------------------
    const getProfile = async () => {
        const [response, data] = await Backend.get(`/api/authors/${user.user_id}/`, authTokens.access);
        if (response.status && response.status === 200) {
            setProfile(data);
        } else if (response.statusText === 'Unauthorized'){
            logoutUser();
        } else {
            console.log('Failed to get profile');
        }
    };

    // event functions -------------------------------------------

    // render functions ------------------------------------------
    const renderProfile = (profile) => {
        if (!profile) {
            return(
                <div>No profile</div>
            );
        } else {
            return(
                <div className='profile'>
                    <table>
                        <thead>
                            <tr>
                                <th>Display Name</th>
                                <th>Node Id</th>
                                <th>GitHub</th>
                                <th>Profile Image</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>{profile.displayName}</td>
                                <td>{profile.id}</td>
                                <td>{profile.github}</td>
                                <td>{profile.profileImage}</td>
                            </tr>
                        </tbody>
                    </table>
                    <br></br>
                    <div>Full Payload: <pre>{JSON.stringify(profile, null, 2)}</pre></div>
                </div>
            );
        }
    };

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
                    <p>You really wanna update?</p>
                    <button onClick={() => setUpdate(false)}>Cancel</button>
                </div>
            )
        }


    }
    // RENDER APP =================================================
    return (
        <>
        {renderProfile(profile)}
        {renderUpdateForm()}
        </>
    );
}

export default Profile;
