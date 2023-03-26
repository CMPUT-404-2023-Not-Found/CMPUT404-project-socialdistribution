import React from 'react'
import Typography from '@mui/material/Typography';
import ReactMarkdown from 'react-markdown'
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
import ListItemAvatar from '@mui/material/ListItemAvatar';

import BasicAvatar from '../common/BasicAvatar/BasicAvatar';

const Comment = (comment) => {
    // no idea why react passes it in like this,
    // makes a new key called comment and assigns the comment object
    // passed in to that
    let commentObj = comment.comment;
    let content = commentObj.comment;
    let contentType = commentObj.contentType;
    console.log(comment);


    const renderCommentBody = (content, contentType) => {
        switch (contentType) {
            case 'text/plain': case 'application/base64': 
                return (
                        <Typography variant='body1' color='text.primary'>{content}</Typography>
                )
            case 'text/markdown':
                return (
                        <ReactMarkdown>{content}</ReactMarkdown>
                )
            default:
                console.error('Got unknown contentType: ', contentType);
                return (
                    <Typography>Unable to render</Typography>
                )
        }
    }

    // This code is adapted from the Material UI docs, retrieved on 2023-03-26
    // https://mui.com/material-ui/react-list/
    return (
        <ListItem alignItems="flex-start">
            <ListItemAvatar>
                <BasicAvatar profile={commentObj.author} size='small'></BasicAvatar>
            </ListItemAvatar>
            <ListItemText
            primary={commentObj.author.displayName}
            secondary={
                renderCommentBody(content, contentType)
            }
            />
        </ListItem>
    )
}

export default Comment
