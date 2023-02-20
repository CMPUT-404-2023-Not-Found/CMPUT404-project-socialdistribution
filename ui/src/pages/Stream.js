import React, { useEffect, useState } from 'react';
// useful explanation about hooks, didn't watch fully because didn't feel like needed all
// all of them
// https://www.youtube.com/watch?v=TNhaISOUy6Q

// button to redirect
// https://stackoverflow.com/questions/50644976/react-button-onclick-redirect-page

// Dynamic linking and fetching from django
// https://www.youtube.com/watch?v=9dwyXq9G_MQ&t=5062s
import { Link, useNavigate } from 'react-router-dom';

const baseURL = 'https://jsonplaceholder.typicode.com';

const Stream = () => {
    let navigate = useNavigate();

    const [posts, setPosts] = useState([]);

    const getPosts = async () => {
        const response = await fetch(`${baseURL}/posts`)

        const data = await response.json()

        if (response.ok) {
            console.log(data)
        } else {
            console.log("Failed network Request")
        }
    }

    useEffect(
        () => {
            getPosts();
        }, []
    )

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