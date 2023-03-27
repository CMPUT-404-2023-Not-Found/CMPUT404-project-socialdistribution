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
import { utcToLocal } from '../../utils/Utils';



const PostHeader = ({ author, title, subheader, time, postId }) => {
    const [ open, setOpen ] = React.useState(false);
    const [ anchorEl, setAnchorEl ] = React.useState(null);
    const navigate = useNavigate();

    console.log(postId);
    const regex = /\/([\w-]+)$/;
    const match = postId.match(regex);
    if (match) {
        const postIdFromUrl = match[1];
        console.log(postIdFromUrl);
    }
    const postIdFromUrl = match[1];

    const menuItems = [
        {
            id: 1,
            label: 'Edit',
            route: '/editpost/' + postIdFromUrl,
        }, 
        {
            id: 2,
            label: 'Delete',
        }
    ];

    const handleClick = (event) => {
        setAnchorEl(event.currentTarget);
        setOpen(true);
      }

    const handleClose = () => {
        setAnchorEl(null);
        setOpen(false);
    };

    // RENDER APP =================================================
    return (
        <CardHeader
            avatar={<BasicAvatar profile={author} size='medium'></BasicAvatar>}
            action={
            <><IconButton aria-label="settings" onClick={handleClick}>
                    <MoreVertIcon />
                </IconButton>
                <BasicMenu
                    open={open}
                    anchorEl={anchorEl}
                    handleClose={handleClose}
                    menuItems={menuItems}
                />
                </>
            }
            title={title}
            titleTypographyProps={postHeaderStyles.cardHeader.titleTypographyProps}
            subheader={(time ? utcToLocal(time) : subheader)}
            subheaderTypographyProps={postHeaderStyles.cardHeader.subheaderTypographyProps}
        />
    )
}

export default PostHeader
