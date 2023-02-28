import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useContext, useState } from 'react';
import AuthContext from '../context/AuthContext';


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

    // form contents
    const [title, setTitle] = useState('');
    const [content, setContent] = useState('');
    const [description, setDescription] = useState('');
    const [contentType, setContentType] = useState('text/plain');
    const [visibility, setVisibility] = useState('PUBLIC');
    const [unlisted, setUnlisted] = useState(false);

    //  async functions -------------------------------------------
    const createPost = async (event) => {
        const request = new Request(
            `${baseURL}/api/authors/${user.user_id}/posts/`,
            {
                body: JSON.stringify({
                    title, content, description, contentType, visibility, unlisted
                }),

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

    const getOptions = async() => {
        const request = new Request(
            `${baseURL}/api/authors/${user.user_id}/posts/`,
            {
                body: JSON.stringify({
                    title, content, description, contentType, visibility, unlisted
                }),

                headers: {
                    'Content-Type':'Application/Json',
                    'Authorization': 'Bearer ' + String(authTokens.access)
                },

                method: 'POST'
            }
        );

        const response = await fetch(request);
    }

    return (
        <>
            <button onClick={() => {
                navigate(-1);
            }}>
                Go back to stream
            </button>

            <form action="" method="post">
                <label htmlFor="title">Title:</label>
                <input type="text" id="title" name="post_title" onChange={(e) => setTitle(e.target.value)}/>
                <br></br>

                <label htmlFor="description">Description:</label>
                <input type="text" id="description" name="post_description" onChange={(e) => setDescription(e.target.value)} />
                <br></br>

                <label htmlFor="content">Content:</label>
                <textarea id="content" name="post_content" style={
                    {
                        verticalAlign: 'top'
                    }
                } onChange={(e) => setContent(e.target.value)}></textarea>
                <br></br>

                <select name="contentType" id="contentType" onChange={(e) => setContentType(e.target.value)}>
                    <option value="">--Content Type--</option>
                    <option value="text/plain">Plain text</option>
                </select>
                <br></br>

                <select name="visibility" id="visibility" onChange={(e) => setVisibility(e.target.value.toUpperCase())}>
                    <option value="">--Visibility--</option>
                    <option value="public">Public</option>
                </select>
                <br></br>

                <input type="checkbox" id="unlisted" name="unlisted" onChange={(e) => {
                    e.target.value === 'on' ? setUnlisted(true) : setUnlisted(false)
                    }}/>
                <label htmlFor="unlisted">Unlisted</label>
                <br></br>

                <button type="button" onClick={createPost}>Send your message</button>
                <br></br>
            </form>

        </>
    );
}

export default CreatePost;