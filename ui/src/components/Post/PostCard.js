/*
2023-03-25
ui/src/components/Post/PostCard.js

*/

import React from 'react';

import BasicCard from '../common/BasicCard/BasicCard';
import PostHeader from './PostHeader';
import PostContent from './PostContent';
import PostActions from './PostActions'

const PostCard = ({ post, source='', ...actions }) => {
    return (
        <BasicCard
            header={
            <PostHeader
                title={post.title ? post.title : post.summary ? post.summary : 'No Title'}
                author={post.author && post.author}
                time={post.updated_at ? post.updated_at : post.published}
            />}
            content={
            <PostContent 
                description={post.description}
                contentType={post.contentType ? post.contentType : post['@context']}
                content={post.content}
                postNodeId={post.id}
            />}
            actions={
                <PostActions 
                    {...actions}
                    postNodeId={post.id}
                    likeCount={post.likeCount ? post.likeCount : null}
                    commentCount={post.commentCount ? post.commentCount : post.count}
                    source={source}
                />}
        />
    );
}

export default PostCard;
