/*
2023-03-13
ui/src/componenets/Navbar/consts/navbarItems.js

This code is modified from a video tutorial on Material UI from theatypicaldeveloper on 2021-11-29, retrieved 2023-03-13 from youtube.com
video here:
https://youtu.be/uLSE7WtcrP0
*/

import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import AllInboxIcon from '@mui/icons-material/AllInbox';
import CreateIcon from '@mui/icons-material/Create';
import EmailIcon from '@mui/icons-material/Email';
import InboxIcon from '@mui/icons-material/Inbox';
import LogoutIcon from '@mui/icons-material/Logout';
import PeopleIcon from '@mui/icons-material/People';

export const mainNavbarItems = [
    {
        id: 0,
        icon: <InboxIcon />,
        label: 'Stream',
        route: '',
    },
    {
        id: 1,
        icon: <AllInboxIcon />,
        label: 'Browse Posts',
        route: 'all',
    },
    {
        id: 2,
        icon: <EmailIcon />,
        label: 'Your Posts',
        route: 'posts',
    },
    {
        id: 3,
        icon: <CreateIcon />,
        label: 'Create a Post',
        route: 'createpost',
    },
    {
        id: 4,
        icon: <PeopleIcon />,
        label: 'Followers',
        route: 'followers',
    }
]

export const secondaryNavbarItems = [
    {
        id: 0,
        icon: <AccountCircleIcon />,
        label: 'Profile',
        route: 'profile',
    },
    {
        id: 1,
        icon: <LogoutIcon />,
        label: 'Logout',
        route: 'login',
    }
]
