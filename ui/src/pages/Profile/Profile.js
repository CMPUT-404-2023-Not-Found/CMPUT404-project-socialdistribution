/*
2023-02-19
pages/Profile.js

This code is modified from a tutorial video about Authentication & Refreshing Tokens from Dennis Ivy on 2022-06-02, retrieved on 2023-02-19, to youtube.com
tutorial video here:
https://www.youtube.com/watch?v=2k8NleFjG7I
*/

import React, { useContext, useEffect, useState } from 'react';
import { CardContent, CardHeader, IconButton, Typography, Box, Button, TextField, FormControl } from '@mui/material';
import GitHubIcon from '@mui/icons-material/GitHub';
import ToolTip from '@mui/material/Tooltip';

import BasicAvatar from '../../components/common/BasicAvatar/BasicAvatar';
import BasicCard from '../../components/common/BasicCard/BasicCard';
import GridWrapper from '../../components/common/GridWrapper/GridWrapper';
import AuthContext from '../../context/AuthContext';
import Backend from '../../utils/Backend';
import PageHeader from '../../components/Page/PageHeader';

import { Snackbar } from '@mui/material';
import MuiAlert from '@mui/material/Alert';



const Profile = () => {
    //  variable declarations -------------------------------------
    const [ displayName, setDisplayName ] = useState('');
    const [ profile, setProfile ] = useState({});
    const [ update, setUpdate ] = useState(false);
    const { user, authTokens, logoutUser } = useContext(AuthContext);
    // Add a new state variable for the GitHub URL
    const [githubUrl, setGithubUrl] = useState('');
    // Snackbar state
    const [snackbarOpen, setSnackbarOpen] = useState(false);
    const [snackbarMessage, setSnackbarMessage] = useState('');
    const [snackbarSeverity, setSnackbarSeverity] = useState('success');
    const Alert = React.forwardRef(function Alert(props, ref) {
        return <MuiAlert elevation={6} ref={ref} variant="filled" {...props} />;
      });
      
      
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
    console.log(user.profileImage)
    console.log(user.github)
    const updateProfile = async (e) => {
        e.preventDefault();
        const postData = JSON.stringify({
            displayName: displayName,
            github: githubUrl // Add the GitHub URL to the post data
        })
        const [response, responseData] = await Backend.post(`/api/authors/${user.user_id}/`, authTokens.access, postData);


        if (response.status && response.status === 200) {
            setProfile(responseData);
            setDisplayName('');
            setUpdate(false);
            setSnackbarMessage("Successfully updated the profile information!");
            setSnackbarSeverity("success");
            setSnackbarOpen(true);
        } else {
            console.log('Failed to post profile');
        }
    };

    const handleCloseSnackbar = (event, reason) => {
        if (reason === 'clickaway') {
            return;
        }
        setSnackbarOpen(false);
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
                    // subheader={profile.host}
                    // subheaderTypographyProps={{ variant: 'h4' }}
                    action={
                    <ToolTip title={(profile.github && profile.github)}>
                    <IconButton size='large' aria-label="github" onClick={() => { console.log(profile.github) }}>
                        <GitHubIcon fontSize='large'/>
                    </IconButton>
                    </ToolTip>
                    }
                />
                <CardContent>
                    <Typography variant='h5'>Host</Typography>
                    <Typography variant='body1'>{profile.host}</Typography>
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
                    <Button variant="contained" color="primary" onClick={() => setUpdate(true)}>
                        Update Account
                    </Button>
                </div>
            );
        } else {
            return (
                <Box sx={{ mt: 3 }}>
                    <form onSubmit={updateProfile}>
                        <FormControl fullWidth>
                            <TextField
                                label="Display Name"
                                id="username"
                                name="username"
                                placeholder="Type your username"
                                defaultValue={profile.displayName || user.username}
                                onChange={(e) => setDisplayName(e.target.value)}
                                sx={{ mb: 2 }}
                            />
                            <TextField
                                label="GitHub URL"
                                id="github-url"
                                name="github-url"
                                placeholder="Type your GitHub URL"
                                defaultValue={profile.github}
                                onChange={(e) => setGithubUrl(e.target.value)}
                                sx={{ mb: 2 }}
                            />
                            <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                                <Button type="submit" variant="contained" color="primary">
                                    Update
                                </Button>
                                <Button variant="outlined" color="secondary" onClick={() => setUpdate(false)}>
                                    Cancel
                                </Button>
                            </Box>
                        </FormControl>
                    </form>
                </Box>
            );
        }
    };

    // RENDER APP =================================================
    return (
        <>
            <PageHeader profile={profile} title='Profile'></PageHeader>
            <GridWrapper>
                {renderProfile()}
                {renderUpdateForm()}
            </GridWrapper>

            <Snackbar
                open={snackbarOpen}
                autoHideDuration={4000}
                onClose={handleCloseSnackbar}
                anchorOrigin={{ vertical: 'top', horizontal: "center" }}
            >
                <Alert onClose={handleCloseSnackbar} severity={snackbarSeverity} sx={{ width: '100%' }}>
                    {snackbarMessage}
                </Alert>
            </Snackbar>
        </>
    );
}

export default Profile;
