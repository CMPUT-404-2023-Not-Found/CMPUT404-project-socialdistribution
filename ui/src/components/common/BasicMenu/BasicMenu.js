/*
2023-03-21
ui/src/components/common/BasicMenu/BasicMenu.js

This code is from a github example of working with MUI by theatypicaldeveloper, last commited 2021-12-22, retrieved on 2023-03-21
github source code here:
https://github.com/theatypicaldeveloper/materialUi-in-react/blob/lesson-4-common-components-completed/src/components/common/BasicMenu/BasicMenu.js
*/
import React from 'react';
import { useNavigate } from 'react-router-dom';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';

const BasicMenu = ({ anchorEl, handleClose, open, menuItems }) => {
    const navigate = useNavigate();

    return (
        <Menu
            id="basic-menu"
            anchorEl={anchorEl}
            open={open}
            onClose={handleClose}
        >
        {menuItems.map((item) => (
          <MenuItem
            key={item.id}
            onClick={() => { navigate(item.route); handleClose() }}
          >
            {item.label}
          </MenuItem>
        ))}
        </Menu>
    );
}

export default BasicMenu;
