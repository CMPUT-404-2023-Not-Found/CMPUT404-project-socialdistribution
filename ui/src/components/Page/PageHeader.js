/*
2023-03-16
ui/src/components/Page/PageHeader.js

*/
import React from 'react';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';

import { menuItems } from './notificationMenuItems';
import NotificationBell from '../common/NotificationBell/NotificationBell';
import { pageStyles } from './styles';

const PageHeader = ({ title, disableNotification=false }) => {
    
    // RENDER APP =================================================
    return (
    <Box sx={pageStyles.PageHeader.wrapper}>
        <Box sx={pageStyles.PageHeader.topRow}>
        { !disableNotification && <NotificationBell iconColor='secondary' badgeContent={4} menuItems={menuItems}/> }
        </Box>
        <Box sx={pageStyles.PageHeader.middleRow}>
            <Typography variant='h4' color='white'>{title}</Typography>
        </Box>
    </Box>
  );
}

export default PageHeader;
