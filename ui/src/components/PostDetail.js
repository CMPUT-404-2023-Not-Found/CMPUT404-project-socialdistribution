import React, { useContext, useEffect, useState } from 'react';
import { useParams } from 'react-router-dom'
import AuthContext from '../context/AuthContext';
import ReactMarkdown from 'react-markdown'

// This code is modified from a tutorial about Routing in React from Joel Olawanle on 2022-09-06, retrieved on 2023-02-19, to hygraph.com
// tutorial here:
// https://hygraph.com/blog/routing-in-react

const PostDetail = () => {

    const {postid} = useParams();

    const [post, setPost] = useState([]);


    const { user, authTokens, logoutUser } = useContext(AuthContext);

    useEffect(
        () => {
            getPost();
        }, [postid]
    )

    const getPost = async () => {
        const getPostsUrl = 'http://localhost:8000/api/authors/' + user.user_id + '/posts/' + postid + '/';

        const response = await fetch(getPostsUrl, {
            headers: {
                'Authorization': 'Bearer ' + String(authTokens.access)
            }
        });

        const data = await response.json();

        if (response.status && response.status === 200) {
            setPost(data);
        } else if (response.statusText === 'Unauthorized'){
            logoutUser();
        } else {
            console.log('Failed to get posts');
        }
    }

    const fullPayload = JSON.stringify(post);

    function getContent(contentType, content)  {
        if (contentType === 'text/plain') {
            return ( 
                // This code is from an answer on StackOverflow from enapupe on 2017-06-07, retrieved on 2023-03-06
                // found here:
                // https://stackoverflow.com/questions/36260013/react-display-line-breaks-from-saved-textarea
                <p style={{
                    whiteSpace: 'pre-line'
                }}>
                    {content}
                </p>
            )
        } else if (contentType === 'text/markdown') {
            return (
                // This code is modified from an answer on GitHub from rexxars on 2017-05-25, retrieved on 2023-03-06
                // found here:
                //https://github.com/remarkjs/react-markdown/issues/174
                <ReactMarkdown components={{
                    img: ({node,...props})=><img style={{maxWidth:'400pt'}}{...props}/>}
                }>
                    {content}
                </ReactMarkdown>
            )
        } else if (contentType === 'application/base64') {
            // for now it should work with .gif or whatever
            return (
                <img src={content}></img>
            )
        } else {
            return (
                <img src={content}></img>
            )
        }
    }
    return (
        <div>
            <h1>Title of the post: {post.title}</h1>

            <p>Description: {post.description}</p>

            {getContent(post.contentType, post.content)}

            <p> This is a ' {post.contentType} ' post</p>
            <p>Full payload: {fullPayload}</p>

        </div>
    )
}

export default PostDetail
