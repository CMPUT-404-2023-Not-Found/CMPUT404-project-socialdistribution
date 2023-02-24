/*
2023-02-24
components/Navbar.js

This code is modified from a tutorial about Routing in React from Joel Olawanle on 2022-09-06, retrieved on 2023-02-19, to hygraph.com
tutorial here:
https://hygraph.com/blog/routing-in-react
*/

import { NavLink } from 'react-router-dom';

const Navbar = () => {
    return ( 
        <nav>
            <div className='navlink'><NavLink to='/'>Home</NavLink></div>
            <span> | </span>
            <div className='navlink'><NavLink to='/login'>Login</NavLink></div>
        </nav>
    );
};

export default Navbar;
