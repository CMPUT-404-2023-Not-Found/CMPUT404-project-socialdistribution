/*
2023-03-13
ui/src/components/Navbar/Navbar.js

This code is modified from a documentation guide on Material UI Drawer components from Material UI SAS 2023, retrieved 2023-03-13 from mui.com
guide here
https://mui.com/material-ui/react-drawer/#full-height-navigation
*/
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
import { Grid } from '@mui/material';

const Navbar = () => {
    let {user, logoutUser} = useContext(AuthContext);
    const navigate = useNavigate();

    if (user) {
        return (
            <Grid item xs={4}>
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
            </Grid>
        );
    }
}

export default Navbar
