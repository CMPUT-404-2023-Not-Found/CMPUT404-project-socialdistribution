/*
2023-02-19
pages/Posts.js

This code is modified from a tutorial video about Authentication & Refreshing Tokens from Dennis Ivy on 2022-06-02, retrieved on 2023-02-19, to youtube.com
tutorial video here:
https://www.youtube.com/watch?v=2k8NleFjG7I
*/

import React, { useContext, useEffect, useState } from 'react';
import { Typography } from '@mui/material';

import Backend from '../../utils/Backend';
import BasicCard from '../../components/common/BasicCard/BasicCard';
import AuthContext from '../../context/AuthContext';
import GridWrapper from '../../components/common/GridWrapper/GridWrapper';
import PostHeader from '../../components/Post/PostHeader';
import PostContent from '../../components/Post/PostContent';
import PageHeader from '../../components/Page/PageHeader';

const YourPosts = () => {
    //  variable declarations -------------------------------------
    const [ posts, setPosts ] = useState([]);
    const { user, authTokens, logoutUser } = useContext(AuthContext);
    
    //  event listners --------------------------------------------
    useEffect(() => {
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
        getPosts();
    }, [user, authTokens, logoutUser]);

    //  async functions -------------------------------------------

    const renderPosts = (items) => {
        if (!items || items.length <= 0) return (<Typography paragraph >No Posts</Typography>);
        let itemsRender = [];
        items.forEach((item, idx) => {
            console.log(item);
            itemsRender.push(
                <BasicCard 
                    key={idx}
                    header={
                        <PostHeader 
                            author={item.author} 
                            title={item.title} 
                            time={(item.updated_at ? item.updated_at : item.published)} 
                        />}
                    content={
                        <PostContent 
                            description={item.description}
                            content={item.content}
                        />}
                />
            );
            itemsRender.push(<br></br>);
        });
        return (<>{itemsRender}</>)
    }
    // RENDER APP =================================================
    return (
        <>
            <PageHeader title='Your Posts'></PageHeader>
            <GridWrapper>
            {renderPosts(posts.items)}
            </GridWrapper>
        </>
    );
}

export default YourPosts;
