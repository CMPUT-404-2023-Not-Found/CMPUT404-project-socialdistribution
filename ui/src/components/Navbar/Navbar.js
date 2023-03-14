import * as React from 'react';
import { useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import Drawer from '@mui/material/Drawer';
import Toolbar from '@mui/material/Toolbar';
import List from '@mui/material/List';
import Divider from '@mui/material/Divider';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';

import AuthContext from '../../context/AuthContext';
import { mainNavbarItems, secondaryNavbarItems } from './consts/navbarItems';
import { navbarStyles } from './consts/styles';

const Navbar = () => {
    let {user, logoutUser} = useContext(AuthContext);
    const navigate = useNavigate();

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
                {mainNavbarItems.map((item, index) => (
                <ListItem key={item.id} onClick={() => navigate(item.route)} disablePadding>
                    <ListItemButton>
                    <ListItemIcon sx={navbarStyles.icons}>
                        {item.icon}
                    </ListItemIcon>
                    <ListItemText primary={item.label} sx={navbarStyles.text} />
                    </ListItemButton>
                </ListItem>
                ))}
            </List>
            <Divider />
            <List>
                {secondaryNavbarItems.map((item, index) => (
                <ListItem 
                    key={item.id} 
                    onClick={item.label === 'Logout' ? logoutUser : () => navigate(item.route)} 
                    disablePadding>
                        <ListItemButton>
                        <ListItemIcon sx={navbarStyles.icons}>
                            {item.icon}
                        </ListItemIcon>
                        <ListItemText primary={item.label} sx={navbarStyles.text} />
                        </ListItemButton>
                </ListItem>
                ))}
            </List>
            </Drawer>
        );
    }
}

export default Navbar
