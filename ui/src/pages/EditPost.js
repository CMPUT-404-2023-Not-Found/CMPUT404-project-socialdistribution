import React from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { useContext, useState, useEffect } from 'react';
import AuthContext from '../context/AuthContext';
import DynamicForm from '../utils/DynamicForm';
import Backend from '../utils/Backend';
import {useForm} from 'react-hook-form';

import GridWrapper from '../components/common/GridWrapper/GridWrapper';
import PageHeader from '../components/Page/PageHeader';

/*
    This code was adapted from a video by Ssali Jonathan, 2022-02-10, retrieved on 2023-02-27, 
    to YouTube: https://www.youtube.com/watch?v=9dwyXq9G_MQ

    I also looked at Mozilla Developer Network's post "Your First Form", to design the form, 
    found here: https://developer.mozilla.org/en-US/docs/Learn/Forms/Your_first_form
*/

const CreatePost = () => {
    //  variable declarations -------------------------------------
    let navigate = useNavigate();

    const currentPost = useParams();

    const { user, authTokens, logoutUser } = useContext(AuthContext);
    
    const [options, setOptions] = useState(null);
    
    const {register, handleSubmit} = useForm();

    //  event listeners --------------------------------------------
    useEffect(() => {
        const getOptions = async () => {
            const [response, data] = await Backend.options(`/api/authors/${user.user_id}/posts/${post_id}`, authTokens.access);
            data.actions.PUT = {
                ...data.actions.PUT,
                'file': {
                    'type' : 'file',
                    'label': 'File',
                    'required': false,
                    'read_only': false,
                }
            }
            setOptions(data);
            console.log(data);
        }

        getOptions();
    }, []);

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

    const editPost = async (formData) => {
        let fileContentTypes = ['image/jpeg;base64', 'image/png;base64', 'application/base64']
        if (fileContentTypes.includes(formData.contentType)) {
            console.log(formData);
            let fileList = formData.file;
    
            let fileBase64 = await getFileData(fileList[0]);

            formData.content =  fileBase64;
        }

        delete formData.file;
        
        const [response, data] = await Backend.post(`/api/authors/${user.user_id}/posts/${post_id}`, authTokens.access, JSON.stringify(formData));
        if (response.status && response.status === 201) {
            navigate('/posts/${post_id}');
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
            {options ?
                    <DynamicForm options={options} formSubmitFunction={editPost}>
                        
                    </DynamicForm>
                    : 
                    <div>
                        Loading form ...
                    </div>
                }
            </GridWrapper>
       </>
    );
}

export default CreatePost;
