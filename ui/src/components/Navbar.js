/*
2023-02-24
components/Navbar.js

This code is modified from a tutorial about Routing in React from Joel Olawanle on 2022-09-06, retrieved on 2023-02-19, to hygraph.com
tutorial here:
https://hygraph.com/blog/routing-in-react
*/

import { useContext } from 'react';
import { NavLink } from 'react-router-dom';

import AuthContext from '../context/AuthContext';

const Navbar = () => {
    let {user, logoutUser} = useContext(AuthContext);
    if (user) {
        return ( 
            <nav>
                <NavLink className='navlink' to='/'>Home</NavLink>
                <span> | </span>
                <NavLink className='navlink' to='/posts'>Your Posts</NavLink>
                <span> | </span>
                <NavLink className='navlink' to='/createpost'>Create Post</NavLink>
                <span> | </span>
                <NavLink className='navlink' to='/profile'>Profile: {user && user.username}</NavLink>
                <span> | </span>
                <NavLink className='navlink' onClick={logoutUser} to='/login'>Logout</NavLink>
            </nav>
        );
    }
};

export default Navbar;
