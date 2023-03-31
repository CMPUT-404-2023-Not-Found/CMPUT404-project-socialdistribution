import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { IconButton, Menu, MenuItem } from '@mui/material';
import MoreVertIcon from '@mui/icons-material/MoreVert';

const PostOptions = ({ postUUID }) => {
    const navigate = useNavigate();
    const [ open, setOpen ] = useState(false);
    const [ anchorEl, setAnchorEl ] = useState(null);
    const menuItems = {
        edit: {
            label: 'Edit',
            route: '/editpost/' + postUUID
        },
        delete: {
            label: 'Delete',
        }
    }

    const handleDelete = () => {

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
            <MenuItem onClick={handleDelete}>{menuItems.delete.label}</MenuItem>
        </Menu>
        </>
    );
}

export default PostOptions;
