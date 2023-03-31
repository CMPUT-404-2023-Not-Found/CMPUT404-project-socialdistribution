/*
2023-03-30
ui/src/pages/EditPost.js

*/

import React, { useContext, useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { Box, Button, FormControlLabel, Checkbox, FormControl, MenuItem, Select, TextField } from '@mui/material';
import InputLabel from '@mui/material/InputLabel';

import AuthContext from '../context/AuthContext';
import Backend from '../utils/Backend';
import GridWrapper from '../components/common/GridWrapper/GridWrapper';
import PageHeader from '../components/Page/PageHeader';
import CommonButton from '../components/common/CommonButton/CommonButton';

const EditPost = () => {
    //  variable declarations -------------------------------------
    let navigate = useNavigate();
    const { postId } = useParams();
    const [ post, setPost ] = useState(null);
    const [ newValues, setNewValues ] = useState({});
    const { user, authTokens, logoutUser } = useContext(AuthContext);

    const contentTypeMenuItems = [
        {value: 'text/markdown', label: 'Markdown'},
        {value: 'text/plain', label: 'Plain Text'}
    ]
    
    const visibilityMenuItems = [
        {value: 'FRIENDS', label: 'Friends'},
        {value: 'PUBLIC', label: 'Public'}
    ];

    const categoriesMenuItems = [
        "business",
        "education",
        "entertainment",
        "finance",
        "health",
        "lifestyle",
        "other",
        "science",
        "sports",
        "technology",
        "travel",
        "tutorial",
        "web",
    ];
    
    //  event listeners --------------------------------------------
    useEffect(() => {
        const getPostData =  async () => {
            const [response, data] = await Backend.get(`/api/authors/${user.user_id}/posts/${postId}`, authTokens.access);
            if (response.status && response.status === 200) {
                console.log('Successfully retrieve post data');
                console.debug(data);
                setPost(data);
            } else if (response.statusText === 'Unauthorized'){
                logoutUser();
            } else {
                console.error('Failed to retrieve post data');
            }
        }

        getPostData();
    }, [postId, user.user_id, authTokens.access, logoutUser]);

    // This code is adapted from a post by Endless on StackOverflow on 2018-01-09, retrieved on 2023-03-17, found here
    // https://stackoverflow.com/questions/48172934/error-using-async-and-await-with-filereader
    const getFileData = (file) => {
        return new Promise((resolve) => {
            const reader = new FileReader();
            reader.onloadend = () => resolve(reader.result);
            reader.readAsDataURL(file);
        })
    }

    const handleSubmit = async (e) => {
        e.preventDefault();
        console.log('Editing post id ' + postId);
        let formData = {};
        return;
        const [response, data] = await Backend.post(`/api/authors/${user.user_id}/posts/${postId}/`, authTokens.access, JSON.stringify(formData));
        if (response.status && response.status === 200) {
            navigate('/posts/');
        } else if (response.statusText === 'Unauthorized'){
            logoutUser();
        } else {
            console.log('Failed to create post');
        }
        console.log(data);
    }

    const handleChange = (e) => {
        const name = e.target.name;
        const value = e.target.value;
        setNewValues((values) => ({ ...values, [name]: value }));
    };

    const handleCheckboxChange = (e) => {
        const name = e.target.name;
        const value = e.target.checked;
        setNewValues((values) => ({ ...values, [name]: value }));

    }

    const showContentType = (contentType, content) => {
        // Don't render images
        if (contentType.startsWith('image') || contentType.startsWith('application') || contentType.startsWith('base64')) {
            return false;
        // Don't render markdown that is only an image
        } else if (content.startsWith('![]')) {
            return false;
        }
        return true;
    };

    return (
        <>
            <PageHeader title='Edit the selected Post'></PageHeader>
            <GridWrapper>
            {post ?
                <Box
                    component='form'
                    noValidate
                    autoComplete='off'
                    sx={{
                        '& > :not(style)': { m: 1 },
                    }}
                >
                    <TextField
                        label='Title'
                        id='title'
                        name='title'
                        defaultValue={post.title}
                        onChange={handleChange}
                        required
                        sx={{ marginBottom: 15, width:"45%" }}
                    />
                    <TextField 
                        label='Description'
                        id='description'
                        name='description'
                        defaultValue={post.description}
                        onChange={handleChange}
                        fullWidth
                        multiline
                        rows={4}
                        sx={{ marginBottom: 15 }}
                    />
                    {showContentType(post.contentType, post.content) &&
                    <>
                    <TextField
                        id='contentType'
                        select
                        label='Content Type'
                        name='contentType'
                        defaultValue={post.contentType} 
                        onChange={handleChange}
                        required
                        sx={{ marginBottom: 15, width:"25%" }}
                    >
                        {contentTypeMenuItems.map((option) => (
                            <MenuItem key={option.value} value={option.value}>{option.label}</MenuItem>
                        ))}
                    </TextField>
                    <TextField 
                        label='Content'
                        id='content'
                        name='content'
                        defaultValue={post.content}
                        onChange={handleChange}
                        fullWidth
                        multiline
                        rows={4}
                    />
                    </>
                    }
                    <TextField
                        id='visibility'
                        label='Visibility'
                        name='visibility'
                        defaultValue={post.visibility && post.visibility}
                        onChange={handleChange}
                        required
                        select
                        fullWidth
                        sx={{ marginBottom: 15, width:"25%" }}
                    >
                    {visibilityMenuItems.map((option) => (
                        <MenuItem key={option.value} value={option.value}>{option.label}</MenuItem>
                    ))}
                    </TextField>
                    <br/>
                    <FormControlLabel 
                        label='Unlisted'
                        labelPlacement='start'
                        control={
                            <Checkbox id='unlisted' name='unlisted' defaultValue={post.unlisted} onChange={handleCheckboxChange} />
                        }
                    />
                    <br/>
                    <CommonButton variant='contained' onClick={handleSubmit}>Update</CommonButton>
                    <CommonButton variant='outlined' onClick={() => { console.log('canceled') }}>Cancel</CommonButton>
                </Box>
                : 
                <div>
                    Loading the selected post ...
                </div>
                }
            </GridWrapper>
       </>
    );
}

export default EditPost;