/*
2023-02-19
pages/Posts.js

This code is modified from a tutorial video about Authentication & Refreshing Tokens from Dennis Ivy on 2022-06-02, retrieved on 2023-02-19, to youtube.com
tutorial video here:
https://www.youtube.com/watch?v=2k8NleFjG7I
*/

import React, { useContext, useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

import Backend from '../utils/Backend';
import PostSummary from '../components/PostSummary';
import AuthContext from '../context/AuthContext';

const Posts = () => {
    //  variable declarations -------------------------------------
    const [ posts, setPosts ] = useState([]);
    const navigate = useNavigate();
    const { user, authTokens, logoutUser } = useContext(AuthContext);
    
    //  event listners --------------------------------------------
    useEffect(() => {
        getPosts();
    }, []);

    //  async functions -------------------------------------------
    const getPosts = async () => {
        const [response, data] = await Backend.get(`/api/authors/${user.user_id}/posts/`, authTokens.access);
        if (response.status && response.status === 200) {
            setPosts(data);
        } else if (response.statusText === 'Unauthorized'){
            logoutUser();
        } else {
            console.log('Failed to get posts');
        }
    };

    const renderPosts = (posts) => {
        if (!posts || posts.length <= 0) {
            return(
                <div>No posts</div>
            );
        } else {
            return(
                <div>
                    {posts.map(post =>(
                        <div key={post.id}>
                            <PostSummary {...post}></PostSummary>
                            <hr></hr>
                        </div> 
                    ))}
                </div>
            );
        }
    };
    // RENDER APP =================================================
    return (
        <>{renderPosts(posts.items)}</>
    );
}

export default Posts;
