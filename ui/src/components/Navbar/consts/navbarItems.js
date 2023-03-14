import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import AllInboxIcon from '@mui/icons-material/AllInbox';
import EmailIcon from '@mui/icons-material/Email';
import InboxIcon from '@mui/icons-material/Inbox';
import LogoutIcon from '@mui/icons-material/Logout';

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
