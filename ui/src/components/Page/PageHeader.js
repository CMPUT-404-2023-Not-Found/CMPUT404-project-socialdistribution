/*
2023-03-16
ui/src/components/Page/PageHeader.js

*/
import React, { useContext, useState, useEffect } from 'react';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';

import AuthContext from '../../context/AuthContext';
import Backend from '../../utils/Backend';
import { menuItems } from './notificationMenuItems';
import NotificationBell from '../common/NotificationBell/NotificationBell';
import { pageStyles } from './styles';

const PageHeader = ({ title, disableNotification=false }) => {
    const [ notification, setNotification ] = useState(0);
    const { user, authTokens, logoutUser } = useContext(AuthContext);

    //  event listners --------------------------------------------
    useEffect(() => {
        const getNotifications = async () => {
            const [response, data] = await Backend.get(`/api/authors/${user.user_id}/inbox/?count`, authTokens.access);
            if (response.status && response.status === 200) {
                console.log('Got notifications data: ');
                console.log(data);
                data.count && setNotification(data.count);
            } else if (response.statusText === 'Unauthorized'){
                logoutUser();
            } else {
                console.log('Failed to get notifications');
            }
        }
        getNotifications();
        const fifthteenMinutes = 5 * 60 * 1000;
        let interval = setInterval(() => {
            getNotifications();
        }, fifthteenMinutes);
        return () => clearInterval(interval);
    }, [notification, user, authTokens, logoutUser])

    // RENDER APP =================================================
    return (
    <Box sx={pageStyles.PageHeader.wrapper}>
        <Box sx={pageStyles.PageHeader.topRow}>
        { !disableNotification && <NotificationBell iconColor='white' badgeContent={notification} menuItems={menuItems}/> }
        </Box>
        <Box sx={pageStyles.PageHeader.middleRow}>
            <Typography variant='h4' color='white'>{title}</Typography>
        </Box>
    </Box>
  );
}

export default PageHeader;
