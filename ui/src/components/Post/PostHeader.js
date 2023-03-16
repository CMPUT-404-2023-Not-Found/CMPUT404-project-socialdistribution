/*
2023-03-15
ui/src/components/Post/PostHeader.js

*/
import React from 'react'
import CardHeader from '@mui/material/CardHeader';
import IconButton from '@mui/material/IconButton';
import MoreVertIcon from '@mui/icons-material/MoreVert';

import BasicAvatar from '../common/BasicAvatar/BasicAvatar';
import { utcToLocal } from '../../utils/Utils';

const PostHeader = ({ author, title, subheader, time }) => {
    // RENDER APP =================================================
    return (
        <CardHeader
            avatar={<BasicAvatar profile={author} size='medium'></BasicAvatar>}
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
