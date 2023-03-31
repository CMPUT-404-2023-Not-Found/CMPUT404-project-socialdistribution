import React, { useContext, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { IconButton, Menu, MenuItem } from '@mui/material';
import MoreVertIcon from '@mui/icons-material/MoreVert';

import AuthContext from '../../context/AuthContext';
import Backend from '../../utils/Backend';
import { getUUIDFromURL } from '../../utils/Utils';

const PostOptions = ({ postNodeId }) => {
    const navigate = useNavigate();
    const postUUID = getUUIDFromURL(postNodeId);
    const { user, authTokens, logoutUser } = useContext(AuthContext);

    const [ open, setOpen ] = useState(false);
    const [ anchorEl, setAnchorEl ] = useState(null);
    const menuItems = {
        edit: {
            label: 'Edit',
            route: '/editpost/' + postUUID
        },
        delete: {
            label: 'Delete',
            sx: {
                color: 'red'
            }
        }
    }

    const handleDelete = async () => {
        let deletePostEndpoint = `/api/authors/${user.user_id}/posts/${postUUID}/`;
        console.debug(`Deleting post at ${deletePostEndpoint}`);
        const response = await Backend.delete(`${deletePostEndpoint}`, authTokens.access);
        if (response.status && response.status === 204) {
            console.log(`Deleted post at ${deletePostEndpoint}`);
            navigate('/posts');
        } else if (response.statusText === 'Unauthorized'){
            logoutUser();
        } else {
            console.error(`Failed to delete post at [${deletePostEndpoint}]`);
        }
        handleClose();
    };

    const handleClick = (event) => {
        setAnchorEl(event.currentTarget);
        setOpen(true);
    };

    const handleClose = () => {
        setAnchorEl(null);
        setOpen(false);
    };

    return (
        <>
        <IconButton aria-label="settings" onClick={handleClick}>
            <MoreVertIcon />
        </IconButton>
        <Menu
            id="basic-menu"
            anchorEl={anchorEl}
            open={open}
            onClose={handleClose}
        >
            <MenuItem onClick={() => { navigate(menuItems.edit.route); handleClose() }}>{menuItems.edit.label}</MenuItem>
            <MenuItem sx={menuItems.delete.sx} onClick={handleDelete}>{menuItems.delete.label}</MenuItem>
        </Menu>
        </>
    );
}

export default PostOptions;
