import React from 'react';
import { useNavigate } from 'react-router-dom';

const CreatePost = () => {
    let navigate = useNavigate();

    return (
        <>
            <div>
                Place holder for post form
            </div>

            <button onClick={() => {
                navigate('/');
            }}>
                Go back to stream
            </button>
        </>
    );
}

export default CreatePost;