/*
2023-03-15
ui/src/components/Post/PostHeader.js

*/
import React from 'react'
import CardHeader from '@mui/material/CardHeader';
import IconButton from '@mui/material/IconButton';
import MoreVertIcon from '@mui/icons-material/MoreVert';
import { useNavigate } from 'react-router-dom';

import BasicAvatar from '../common/BasicAvatar/BasicAvatar';
import BasicMenu from '../common/BasicMenu/BasicMenu';
import { postHeaderStyles } from './styles';
import { getUUIDFromURL, utcToLocal } from '../../utils/Utils';
import PostOptions from './PostOptions';

const PostHeader = ({ author, title, subheader, time, postNodeId }) => {
    const postUUID = getUUIDFromURL(postNodeId);

    // RENDER APP =================================================
    return (
        <CardHeader
            avatar={<BasicAvatar profile={author} size='medium'></BasicAvatar>}
            action={<PostOptions postUUID={postUUID}></PostOptions>}
            title={title}
            titleTypographyProps={postHeaderStyles.cardHeader.titleTypographyProps}
            subheader={(time ? utcToLocal(time) : subheader)}
            subheaderTypographyProps={postHeaderStyles.cardHeader.subheaderTypographyProps}
        />
    )
}

export default PostHeader
