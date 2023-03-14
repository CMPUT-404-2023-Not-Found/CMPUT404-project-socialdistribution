import * as React from 'react';
import { useContext } from 'react';
import Drawer from '@mui/material/Drawer';
import Toolbar from '@mui/material/Toolbar';
import List from '@mui/material/List';
import Divider from '@mui/material/Divider';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import InboxIcon from '@mui/icons-material/MoveToInbox';
import MailIcon from '@mui/icons-material/Mail';

import AuthContext from '../../context/AuthContext';
import { mainNavbarItems, secondaryNavbarItems } from './consts/navbarItems';
import { navbarStyles } from './consts/styles';

const Navbar = () => {
    const drawerWidth = 220;
    let {user, logoutUser} = useContext(AuthContext);
    if (user) {
        return (
            <Drawer
            sx={navbarStyles.drawer}
            variant="permanent"
            anchor="left"
            >
            <Toolbar />
            <Divider />
            <List>
                {mainNavbarItems.map((text, index) => (
                <ListItem key={text.id} disablePadding>
                    <ListItemButton>
                    <ListItemIcon sx={navbarStyles.icons}>
                        {text.icon}
                    </ListItemIcon>
                    <ListItemText primary={text.label} sx={navbarStyles.text} />
                    </ListItemButton>
                </ListItem>
                ))}
            </List>
            <Divider />
            <List>
                {secondaryNavbarItems.map((text, index) => (
                <ListItem key={text.id} disablePadding>
                    <ListItemButton>
                    <ListItemIcon sx={navbarStyles.icons}>
                        {text.icon}
                    </ListItemIcon>
                    <ListItemText primary={text.label} sx={navbarStyles.text} />
                    </ListItemButton>
                </ListItem>
                ))}
            </List>
            </Drawer>
        );
    }
}

export default Navbar
