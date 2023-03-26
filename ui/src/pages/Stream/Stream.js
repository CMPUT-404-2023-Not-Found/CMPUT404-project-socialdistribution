/*
2023-03-13
ui/src/pages/Stream/Stream.js

*/

import React, { useState } from 'react';
import Typography from '@mui/material/Typography';

import BasicPagination from '../../components/common/BasicPagination/BasicPagination';
import GridWrapper from '../../components/common/GridWrapper/GridWrapper';
import PostCard from '../../components/Post/PostCard';
import PageHeader from '../../components/Page/PageHeader';

const Stream = () => {
    //  variable declarations -------------------------------------
    const postEndpoint = '/api/posts';
    const itemResultsKey = 'items';
    const [ nodePosts, setNodePosts ] = useState([]);

    // RENDER APP =================================================
    const renderNodePosts = (items) => {
        if (!items || items.length <= 0) return (<Typography paragraph >No Posts</Typography>);
        let itemsRender = [];
        items.forEach((item, idx) => {
            console.log(item);
            itemsRender.push(<PostCard key={idx * 2} post={item} />);
            itemsRender.push(<br key={idx * 2 + 1} />);
        });
        return (<>{itemsRender}</>)
    };

    return (
        <>
            <PageHeader title='Stream'></PageHeader>
            <GridWrapper>
            {renderNodePosts(nodePosts)}
            <BasicPagination 
                itemEndpoint={postEndpoint} 
                itemResultsKey={itemResultsKey} 
                setItems={(posts) => setNodePosts(posts)}
            />
            </GridWrapper>
        </>
    );
}

export default Stream;
