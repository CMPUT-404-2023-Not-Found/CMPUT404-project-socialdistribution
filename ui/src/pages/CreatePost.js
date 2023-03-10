import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useContext, useState, useEffect } from 'react';
import AuthContext from '../context/AuthContext';
import DynamicForm from '../utils/DynamicForm';
import Backend from '../utils/Backend';
import {useForm} from 'react-hook-form';

/*
    This code was adapted from a video by Ssali Jonathan, 2022-02-10, retrieved on 2023-02-27, 
    to YouTube: https://www.youtube.com/watch?v=9dwyXq9G_MQ

    I also looked at Mozilla Developer Network's post "Your First Form", to design the form, 
    found here: https://developer.mozilla.org/en-US/docs/Learn/Forms/Your_first_form
*/

const CreatePost = () => {
    //  variable declarations -------------------------------------
    let navigate = useNavigate();

    const { user, authTokens, logoutUser } = useContext(AuthContext);
    
    const [options, setOptions] = useState(null);
    
    const {register, handleSubmit} = useForm();

    //  event listeners --------------------------------------------
    useEffect(() => {
        const getOptions = async () => {
            const [response, data] = await Backend.options(`/api/authors/${user.user_id}/posts/`, authTokens.access);
            setOptions(data);
            console.log(data);
        }

        getOptions();
    }, []);

    //  async functions -------------------------------------------
    const createPost = async (formData) => {
        const [response, data] = await Backend.post(`/api/authors/${user.user_id}/posts/`, authTokens.access, JSON.stringify(formData));
        if (response.status && response.status === 201) {
            navigate('/posts');
        } else if (response.statusText === 'Unauthorized'){
            logoutUser();
        } else {
            console.log('Failed to create post');
        }
    }


    // did this because options depends on the async function,
    // so if you pass null to dynamic form it gives an error
    // not sure of another way to fix it
    return (
       <>
       {options ?
            <DynamicForm options={options} formSubmitFunction={createPost}></DynamicForm>
            : 
            <div>
                Loading form ...
            </div>
        }
       </>
    );
}

export default CreatePost;
