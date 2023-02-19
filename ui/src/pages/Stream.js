import React from 'react';
// useful explanation about hooks, didn't watch fully because didn't feel like needed all
// all of them
// https://www.youtube.com/watch?v=TNhaISOUy6Q

// button to redirect
// https://stackoverflow.com/questions/50644976/react-button-onclick-redirect-page
import { Link, useNavigate } from 'react-router-dom';

const Stream = () => {
    let navigate = useNavigate();

    return (
        <>
        <div>
            Place holder for stream
        </div>

        <button onClick={() => {
            navigate('/createpost');
        }}>
            Make a post
        </button>

        <br/>
        <button onClick={() => {
            navigate('/post')
        }}> 
            View a post
        </button>

        </>
    );
}

export default Stream;