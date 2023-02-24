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
    let {user} = useContext(AuthContext);
    return ( 
        <nav>
            <div className='navlink'><NavLink to='/'>Home</NavLink></div>
            <span> | </span>
            { user ? (
                <div className='navlink'><p>Logout</p></div>
            ) : (
                <div className='navlink'><NavLink to='/login'>Login</NavLink></div>
            )}

            { user && <h2>Hello {user.displayName}</h2>}
        </nav>
    );
};

export default Navbar;
