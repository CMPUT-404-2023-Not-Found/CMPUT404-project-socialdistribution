/*
2023-02-19
pages/Posts.js

This code is modified from a tutorial video about Authentication & Refreshing Tokens from Dennis Ivy on 2022-06-02, retrieved on 2023-02-19, to youtube.com
tutorial video here:
https://www.youtube.com/watch?v=2k8NleFjG7I
*/

import React, { useContext, useState } from 'react';
import Typography from '@mui/material/Typography';

import AuthContext from '../../context/AuthContext';
import BasicPagination from '../../components/common/BasicPagination/BasicPagination';
import GridWrapper from '../../components/common/GridWrapper/GridWrapper';
import PostCard from '../../components/Post/PostCard';
import PageHeader from '../../components/Page/PageHeader';

const YourPosts = () => {
    //  variable declarations -------------------------------------
    const [ posts, setPosts ] = useState([]);
    const { user } = useContext(AuthContext);
    const postEndpoint = `/api/authors/${user.user_id}/posts`;
    const itemResultsKey = 'items';

    //  async functions -------------------------------------------

    const renderPosts = (items) => {
        if (!items || items.length <= 0) return (<Typography paragraph >No Posts</Typography>);
        let itemsRender = [];
        items.forEach((item, idx) => {
            console.log(item);
            itemsRender.push(<PostCard key={idx * 2} post={item} disableLike />);
            itemsRender.push(<br key={idx * 2 + 1}/>);
        });
        console.log(itemsRender)
        return (<>{itemsRender}</>)
    }
    // RENDER APP =================================================
    return (
        <>
            <PageHeader title='Your Posts'></PageHeader>
            <GridWrapper>
            <BasicPagination 
                itemEndpoint={postEndpoint} 
                itemResultsKey={itemResultsKey} 
                setItems={(posts) => setPosts(posts)}
            />
            {renderPosts(posts)}
            </GridWrapper>
        </>
    );
}

export default YourPosts;
