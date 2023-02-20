import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useState } from 'react';

const CreatePost = () => {
    let navigate = useNavigate();

    const [title, setTitle] = useState('');
    const [content, setContent] = useState('');
    const [description, setDescription] = useState('');
    const [contentType, setContentType] = useState('');
    const [visibility, setVisibility] = useState('');
    const [unlisted, setUnlisted] = useState(false);

    const createPost = () => {
        console.log(title);
        console.log(content);
        console.log(description);
        console.log(contentType);
        console.log(visibility);
        console.log(unlisted);
    }

    return (
        <>
            <button onClick={() => {
                navigate('/');
            }}>
                Go back to stream
            </button>

            <form action="" method="post">
                <label for="title">Title:</label>
                <input type="text" id="title" name="post_title" onChange={(e) => setTitle(e.target.value)}/>
                <br></br>

                <label for="description">Description:</label>
                <input type="text" id="description" name="post_description" onChange={(e) => setDescription(e.target.value)} />
                <br></br>

                <label for="content">Content:</label>
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

                <select name="visibility" id="visibility" onChange={(e) => setVisibility(e.target.visibility)}>
                    <option value="">--Visibility--</option>
                    <option value="public">Public</option>
                </select>
                <br></br>

                <input type="checkbox" id="unlisted" name="unlisted" onChange={(e) => setUnlisted(e.target.visibility)}/>
                <label for="unlisted">Unlisted</label>
                <br></br>

                <button type="button" onClick={createPost()}>Send your message</button>
                <br></br>
            </form>

        </>
    );
}

export default CreatePost;