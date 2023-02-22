import React, { useEffect, useState } from 'react';
// useful explanation about hooks, didn't watch fully because didn't feel like needed all
// all of them
// https://www.youtube.com/watch?v=TNhaISOUy6Q

// button to redirect
// https://stackoverflow.com/questions/50644976/react-button-onclick-redirect-page

// Dynamic linking and fetching from django
// https://www.youtube.com/watch?v=9dwyXq9G_MQ&t=5062s
import { Link, useNavigate } from 'react-router-dom';
import PostSummary from '../components/PostSummary';

const baseURL = 'http://localhost:8000';
const authoruuid = 'de52020f-f5df-4361-b771-2829a99f16a2';

const Stream = () => {
    let navigate = useNavigate();

    const [posts, setPosts] = useState([]);

    const getPosts = async () => {
        const response = await fetch(`${baseURL}/api/authors/${authoruuid}/posts`)

        const data = await response.json()

        if (response.ok) {
            console.log(data)
            setPosts(data)
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

            <div>
            { posts.length > 0 ? (
                posts.map( (post) => {
                    return (
                        <div key={post.id}>
                            <PostSummary 
                                authorobject={post.author_id}
                                description={post.description}
                                postid={post.id}
                            />
                            <br/>
                        </div>
                    )
                })
            ) : (
                <div>No posts</div>
            ) }
            </div>

        </>
    );
}

export default Stream;