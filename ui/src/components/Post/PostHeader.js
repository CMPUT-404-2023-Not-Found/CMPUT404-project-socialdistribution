/*
2023-03-15
ui/src/components/Post/PostHeader.js

*/
import React from 'react'
import Avatar from '@mui/material/Avatar';
import CardHeader from '@mui/material/CardHeader';
import IconButton from '@mui/material/IconButton';
import MoreVertIcon from '@mui/icons-material/MoreVert';

import { utcToLocal } from '../../utils/Utils';

const PostHeader = ({ author, title, subheader, time }) => {
    // RENDER APP =================================================
    const renderAvatar = (author) => {
        let authorName = (author.displayName ? author.displayName : author.username);
        let authorNameShort = authorName.charAt(0);
        if (author.profileImage) {
            return (
            <Avatar alt={authorName} src={author.profileImage}></Avatar>
            )
        } else {
            return (
            <Avatar sx={{ bgcolor: 'primary.main' }}>{authorNameShort}</Avatar>
            )
        }
    }
    return (
        <CardHeader
            avatar={renderAvatar(author)}
            action={
            <IconButton aria-label="settings">
                <MoreVertIcon />
            </IconButton>
            }
            title={title}
            subheader={(time ? utcToLocal(time) : subheader)}
        />
    )
}

export default PostHeader
