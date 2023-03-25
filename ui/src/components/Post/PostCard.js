/*
2023-03-25
ui/src/components/Post/PostCard.js

*/

import React from 'react';

import BasicCard from '../common/BasicCard/BasicCard';
import PostHeader from './PostHeader';
import PostContent from './PostContent';
import PostActions from './PostActions';

const PostCard = ({ post, ...actions }) => {
    return (
        <BasicCard
            header={
            <PostHeader
                title={post.title ? post.title : 'No title'}
                author={post.author && post.author}
                time={post.updated_at ? post.updated_at : post.published}
            />}
            content={
            <PostContent 
                description={post.description}
                contentType={post.contentType}
                content={post.content}
                postNodeId={post.id}
            />}
            actions={
                <PostActions 
                    {...actions}
                    postNodeId={post.id}
                />}
        />
    );
}

export default PostCard;
