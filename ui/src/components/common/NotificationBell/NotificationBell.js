/*
2023-03-21

This code is modified from a github example of a notification bell in MUI by theatypicaldeveloper, last commited 2021-12-22, retrieved on 2023-03-21
github source code here:
https://github.com/theatypicaldeveloper/materialUi-in-react/blob/lesson-4-common-components-completed/src/components/common/NotificationBell/NotificationBell.js
*/
import React from 'react';
import Badge from '@mui/material/Badge'
import IconButton from '@mui/material/IconButton';
import NotificationsIcon from '@mui/icons-material/Notifications';
import { Tooltip } from '@mui/material';

const NotificationBell = ({ iconColor, badgeContent }) => {
    const newNotification = `You have ${badgeContent} new notifications`;
    const noNewNotification = 'No new notifications';
    return (
            <Tooltip title={badgeContent ? newNotification : noNewNotification}>
                <IconButton color={iconColor}>
                    <Badge
                        badgeContent={badgeContent}
                        color='error'
                        >
                        <NotificationsIcon/>
                    </Badge>
                </IconButton>
            </Tooltip>
  );
}

export default NotificationBell;
