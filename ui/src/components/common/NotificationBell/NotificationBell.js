/*
2023-03-21
ui/src/components/common/NotificationBell/NotificationBell.js

This code is from a github example of working with MUI by theatypicaldeveloper, last commited 2021-12-22, retrieved on 2023-03-21
github source code here:
https://github.com/theatypicaldeveloper/materialUi-in-react/blob/lesson-4-common-components-completed/src/components/common/NotificationBell/NotificationBell.js
*/
import React, { useState } from 'react';
import Badge from '@mui/material/Badge'
import IconButton from '@mui/material/IconButton';
import NotificationsIcon from '@mui/icons-material/Notifications';
import Tooltip from '@mui/material/Tooltip';

import BasicMenu from '../BasicMenu/BasicMenu';

const NotificationBell = ({ iconColor, badgeContent, menuItems }) => {
    //  variable declarations -------------------------------------
    const newNotification = `You have ${badgeContent} new notifications`;
    const noNewNotification = 'No new notifications';
    const [ open, setOpen ] = useState(false);
    const [ anchorEl, setAnchorEl ] = useState(null);

    //  event listners --------------------------------------------
    //  async functions -------------------------------------------
    //  functions -------------------------------------------------
    const handleOpen = (e) => {
        setAnchorEl(e.currentTarget);
        setOpen(true);
    };

    const handleClose = () => {
        setAnchorEl(null);
        setOpen(false);
    };

    return (
            <>
            <Tooltip title={badgeContent ? newNotification : noNewNotification}>
                <IconButton 
                    sx={{color: iconColor}}
                    onClick={badgeContent ? handleOpen : null}
                    anchorEl={anchorEl}
                >
                    <Badge
                        badgeContent={badgeContent}
                        color='error'
                        >
                        <NotificationsIcon/>
                    </Badge>
                </IconButton>
            </Tooltip>
            <BasicMenu
                open={open}
                anchorEl={anchorEl}
                handleClose={handleClose}
                menuItems={menuItems}
            />
            </>
  );
}

export default NotificationBell;
