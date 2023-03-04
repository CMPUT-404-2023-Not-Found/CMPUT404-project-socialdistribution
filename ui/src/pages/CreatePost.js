import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useContext, useState, useEffect } from 'react';
import AuthContext from '../context/AuthContext';
import DynamicForm from '../utils/DynamicForm';
import {useForm} from 'react-hook-form';

const baseURL = 'http://localhost:8000';

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
            const request = new Request(
                `${baseURL}/api/authors/${user.user_id}/posts/`,
                {
                    headers: {
                        'Authorization': 'Bearer ' + String(authTokens.access)
                    },

                    method: 'OPTIONS'
                }
            );

            const response = await fetch(request);
            const data = await response.json();
            setOptions(data);
            console.log(data);
        }

        getOptions();
    }, []);

    //  async functions -------------------------------------------
    const createPost = async (formData) => {
        const request = new Request(
            `${baseURL}/api/authors/${user.user_id}/posts/`,
            {
                body: JSON.stringify(formData),

                headers: {
                    'Content-Type':'Application/Json',
                    'Authorization': 'Bearer ' + String(authTokens.access)
                },

                method: 'POST'
            }
        );

        const response = await fetch(request);
        
        console.log(response);
        if (response.status && response.status === 201) {
            navigate(-1);
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