import React from 'react';
import { useNavigate, useParams, useLocation } from 'react-router-dom';
import { useContext, useState, useEffect } from 'react';
import AuthContext from '../context/AuthContext';
import DynamicForm from '../utils/DynamicForm';
import Backend from '../utils/Backend';
import {useForm} from 'react-hook-form';

import GridWrapper from '../components/common/GridWrapper/GridWrapper';
import PageHeader from '../components/Page/PageHeader';
import { MenuItem, Select, TextField } from '@mui/material';
import SelectInput from '@mui/material/Select/SelectInput';
import InputLabel from '@mui/material/InputLabel';

/*
    This code was adapted from a video by Ssali Jonathan, 2022-02-10, retrieved on 2023-02-27, 
    to YouTube: https://www.youtube.com/watch?v=9dwyXq9G_MQ

    I also looked at Mozilla Developer Network's post "Your First Form", to design the form, 
    found here: https://developer.mozilla.org/en-US/docs/Learn/Forms/Your_first_form
*/

const EditPost = () => {
    //  variable declarations -------------------------------------
    let navigate = useNavigate();
    const{ postId } = useParams(); // recieve the selected post id from PostHeader.js
    // console.log(postId);

    const [ post, setPost ] = useState(null);
    const { user, authTokens, logoutUser } = useContext(AuthContext);

    const contentTypeMenuItems = [
        {id: 1, value: 'text/plain', label: 'Text'},
        {id: 2, value: 'text/markdown', label: 'Markdown'},
        {id: 3, value: 'image/jpeg;base64', label: 'JPEG'},
        {id: 4, value: 'image/png;base64', label: 'PNG'},
        {id: 5, value: 'application/base64', label: 'Base64'},
    ]
    
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

    //  async functions -------------------------------------------

    // This code is adapted from a post by Endless on StackOverflow on 2018-01-09, retrieved on 2023-03-17, found here
    // https://stackoverflow.com/questions/48172934/error-using-async-and-await-with-filereader
    const getFileData = (file) => {
        return new Promise((resolve) => {
            const reader = new FileReader();
            reader.onloadend = () => resolve(reader.result);
            reader.readAsDataURL(file);
        })
    }

    const handleSubmit = async (formData) => {
        formData.preventDefault();
        let fileContentTypes = ['image/jpeg;base64', 'image/png;base64', 'application/base64'];
        console.log('Editing post id ' + postId);
        console.log(formData);
        // if the content type is a file upload, then get the file data
        if (fileContentTypes.includes(formData.contentType)) {
            console.log('File detected, retreiving file data');
            let fileList = formData.file;
            let fileBase64 = await getFileData(fileList[0]);
            formData.content =  fileBase64;
        }

        delete formData.file;
        
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


    // did this because options depends on the async function,
    // so if you pass null to dynamic form it gives an error
    // not sure of another way to fix it

    return (
        <>
            <PageHeader title='Edit the selected Post'></PageHeader>
            <GridWrapper>
            {post ?
                <form onSubmit={handleSubmit}>
                    <TextField 
                        label='Title'
                        id='title'
                        name='title'
                        defaultValue={post.title}
                    />
                    <TextField 
                        label='Description'
                        id='description'
                        name='description'
                        defaultValue={post.description}
                    />
                    <InputLabel id="contentType">Content Type</InputLabel>
                    <Select
                        label='Content Type'
                        id='contentType'
                        name='contentType'
                        defaultValue={post.contentType} 
                    >
                        {contentTypeMenuItems.map((item) => (
                            <MenuItem key={item.id} value={item.value}>{item.label}</MenuItem>
                        ))}
                    </Select>

                </form>
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
