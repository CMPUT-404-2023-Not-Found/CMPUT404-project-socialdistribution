import React from 'react'
import { useParams } from 'react-router-dom'
import { useState, useEffect} from 'react';

const baseURL = 'http://localhost:8000';
const authoruuid = 'de52020f-f5df-4361-b771-2829a99f16a2';

const PostDetail = () => {

    const {postid} = useParams();

    const [post, setPost] = useState([]);

    const getPost = async () => {
        const response = await fetch(`${baseURL}/api/authors/${authoruuid}/posts/${postid}`);

        const data = await response.json();

        if (response.ok) {
            console.log(data);
            setPost(data);
        } else {
            console.log("Failed network Request")
        }
    }

    useEffect(
        () => {
            getPost();
        }, [postid]
    )

    return (
        <div>
        placehodler for a detailed post - {post.author_id}
        <br></br>
        title is: {post.title}
        <br></br>
        content is : {post.content}
        <br></br>
        was posted on : {post.published}
        </div>
    )
}

export default PostDetail