/*
2023-03-13
ui/src/pages/Stream/Stream.js

*/

import React, { useContext, useEffect, useState } from 'react';
import { Typography } from '@mui/material';

import Backend from '../../utils/Backend';
import AuthContext from '../../context/AuthContext';
import BasicCard from '../../components/common/BasicCard/BasicCard';
import GridWrapper from '../../components/common/GridWrapper/GridWrapper';
import PostCard from '../../components/Post/PostCard';
import PageHeader from '../../components/Page/PageHeader';

const Stream = () => {
    //  variable declarations -------------------------------------
    const [ nodePosts, setNodePosts ] = useState({});
    const { authTokens, logoutUser } = useContext(AuthContext);

    //  event listners --------------------------------------------
    useEffect(() => {
        const getNodePosts = async () => {
            const [response, data] = await Backend.get(`/api/posts/`, authTokens.access);
            if (response.status && response.status === 200) {
                console.log(data)
                setNodePosts(data);
            } else if (response.statusText === 'Unauthorized'){
                logoutUser();
            } else {
                console.log('Failed to get posts');
            }
        };
        getNodePosts();
    }, [authTokens, logoutUser]);

    // RENDER APP =================================================
    const renderNodePosts = (items) => {
        if (!items || items.length <= 0) return (<Typography paragraph >No Posts</Typography>);
        let itemsRender = [];
        items.forEach((item, idx) => {
            console.log(item);
            itemsRender.push(<PostCard key={idx} post={item} actions={{likeable: true, shareable: true}}/>);
            itemsRender.push(<br key={idx + items.length}></br>);
        });
        return (<>{itemsRender}</>)
    };

    return (
        <>
            <PageHeader title='Stream'></PageHeader>
            <GridWrapper>
            {renderNodePosts(nodePosts.items)}
            </GridWrapper>
        </>
    );
}

export default Stream;
