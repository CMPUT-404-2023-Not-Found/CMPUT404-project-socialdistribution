/*
2023-02-19
pages/Profile.js

This code is modified from a tutorial video about Authentication & Refreshing Tokens from Dennis Ivy on 2022-06-02, retrieved on 2023-02-19, to youtube.com
tutorial video here:
https://www.youtube.com/watch?v=2k8NleFjG7I
*/

import React, { useContext, useEffect, useState } from 'react';
import { CardContent, CardHeader, IconButton, Typography, Box, Button, TextField, FormControl,InputAdornment ,Tooltip} from '@mui/material';
import GitHubIcon from '@mui/icons-material/GitHub';

import BasicCard from '../../components/common/BasicCard/BasicCard';
import GridWrapper from '../../components/common/GridWrapper/GridWrapper';
import AuthContext from '../../context/AuthContext';
import Backend from '../../utils/Backend';
import PageHeader from '../../components/Page/PageHeader';
import AuthorCard from '../../components/Author/AuthorCard';
import BasicAvatar from '../../components/common/BasicAvatar/BasicAvatar';


import { Snackbar } from '@mui/material';
import MuiAlert from '@mui/material/Alert';
import HighlightOffIcon from '@mui/icons-material/HighlightOff';




const Profile = () => {
    //  variable declarations -------------------------------------
    const [inputs, setInputs] = useState({});
    const [ profile, setProfile ] = useState({});
    const [ update, setUpdate ] = useState(false);
    const { user, authTokens, logoutUser } = useContext(AuthContext);
    // Add a new state variable for the GitHub URL
    // const [githubUrl, setGithubUrl] = useState('');
    // const [ displayName, setDisplayName ] = useState('');
    // Snackbar state
    const [snackbarOpen, setSnackbarOpen] = useState(false);
    const [snackbarMessage, setSnackbarMessage] = useState('');
    const [snackbarSeverity, setSnackbarSeverity] = useState('success');
    const Alert = React.forwardRef(function Alert(props, ref) {
        return <MuiAlert elevation={6} ref={ref} variant="filled" {...props} />;
      });

    const handleClear = (inputName) => {
    setInputs((values) => ({ ...values, [inputName]: '' }));
    };
        
      
    //  event listners --------------------------------------------
    useEffect(() => {
        const getProfile = async () => {
            const [response, data] = await Backend.get(`/api/authors/${user.user_id}/`, authTokens.access);
            if (response.status && response.status === 200) {
                console.log('Got profile');
                console.log(data);
                setProfile(data);
                setInputs({ displayName: data.displayName || '', githubUrl: data.github || '' , profileImage: data.profileImage || ''});
            } else if (response.statusText === 'Unauthorized'){
                logoutUser();
            } else {
                console.log('Failed to get profile');
            }
        };
        getProfile();
    }, [ user, authTokens, logoutUser ]);

    const handleChange = (event) => {
        const name = event.target.name;
        const value = event.target.value;
        setInputs((values) => ({ ...values, [name]: value }));
    };

    const handleSubmit = (event) => {
        event.preventDefault();
        updateProfile(event); // Call the updateProfile function here
      };

    //  async functions -------------------------------------------
    console.log(profile.profileImage)
    console.log(profile.github)
    const updateProfile = async (e) => {
        e.preventDefault();
        const postData = JSON.stringify({
            // displayName: displayName,
            // github: githubUrl // Add the GitHub URL to the post data
            displayName: inputs.displayName,
            github: inputs.githubUrl,
            profileImage: inputs.profileImage 
        })
        const [response, responseData] = await Backend.post(`/api/authors/${user.user_id}/`, authTokens.access, postData);
        const changes = {};

        // Add displayName to the changes if it has a value
        if (inputs.displayName) {
            changes.displayName = inputs.displayName;
        }

        // Add githubUrl to the changes if it has a value
        if (inputs.githubUrl) {
            changes.github = inputs.githubUrl;
        }

        if (inputs.profileImage) {
            changes.profileImage = inputs.profileImage;
        }
        // Check if there are any changes before sending the request
        if (Object.keys(changes).length === 0) {
            console.log('No changes to submit');
            return;
        }

        if (response.status && response.status === 200) {
            setProfile(responseData);
            // setDisplayName('');
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
                    <CardHeader title='Oops' subheader="Couldn't Find Profile"></CardHeader>
                    <CardContent></CardContent>
                </BasicCard>
            )
        }
        let profileTitle = (profile.displayName ? profile.displayName : user.username)
        return (
            <BasicCard>
                <CardHeader
                    titleTypographyProps={{ variant: 'h3', textAlign: 'center', mt: 2 }}
                    title={profileTitle}
                />
                <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', pb: 3 }}>
                    <BasicAvatar key={profile.profileImage} profile={profile} size='large' />
                    <Box mt={2}>
                        <Tooltip title={profile.github ? profile.github : ''}>
                            <IconButton
                                size='large'
                                aria-label="github"
                                component="a"
                                href={profile.github ? profile.github : '#'}
                                target="_blank"
                                rel="noopener noreferrer"
                            >
                                <GitHubIcon fontSize='large' />
                            </IconButton>
                        </Tooltip>
                    </Box>
                </Box>
                <CardContent>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                        <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-start', marginRight: 4 }}>
                            <Typography variant='h6'>Username</Typography>
                            <Typography variant='h6'>Host</Typography>
                            <Typography variant='h6'>ID</Typography>
                        </Box>
                        <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-start' }}>
                            <Typography variant='body1'>{user.username}</Typography>
                            <Typography variant='body1'>{profile.host}</Typography>
                            <Typography variant='body1'>{profile.url}</Typography>
                        </Box>
                    </Box>
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
                    <form onSubmit={handleSubmit}>
                        <FormControl fullWidth>
                            <TextField
                                label="Display Name"
                                id="displayName"
                                name="displayName"
                                placeholder={profile.displayName || "Type your display name"}
                                value={inputs.displayName || ''}
                                required
                                onChange={handleChange}
                                sx={{ mb: 2 }}
                                InputProps={{
                                    endAdornment: (
                                    <InputAdornment position="end">
                                        <IconButton
                                        edge="end"
                                        onClick={() => handleClear('displayName')}
                                        >
                                        < HighlightOffIcon />
                                        </IconButton>
                                    </InputAdornment>
                                    ),
                                }}
                            />
                            <TextField
                                label="GitHub URL"
                                id="githubUrl"
                                name="githubUrl"
                                placeholder={profile.github || "Type your GitHub URL"}
                                value={inputs.githubUrl || ''}
                                required
                                onChange={handleChange}
                                sx={{ mb: 2 }}
                                InputProps={{
                                    endAdornment: (
                                    <InputAdornment position="end">
                                        <IconButton
                                        edge="end"
                                        onClick={() => handleClear('githubUrl')}
                                        >
                                        < HighlightOffIcon />
                                        </IconButton>
                                    </InputAdornment>
                                    ),
                                }}
                             />
                             <TextField
                                label="Profile Image URL"
                                id="profileImage"
                                name="profileImage"
                                placeholder={profile.profileImage || "Type your profile image URL"}
                                value={inputs.profileImage || ''}
                                required
                                onChange={handleChange}
                                sx={{ mb: 2 }}
                                InputProps={{
                                    endAdornment: (
                                    <InputAdornment position="end">
                                        <IconButton
                                        edge="end"
                                        onClick={() => handleClear('profileImage')}
                                        >
                                        < HighlightOffIcon />
                                        </IconButton>
                                    </InputAdornment>
                                    ),
                                }}
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
        };

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
