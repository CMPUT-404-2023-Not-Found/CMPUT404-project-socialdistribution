/*
2023-02-19
App.js

This code is modified from a tutorial about Routing in React from Joel Olawanle on 2022-09-06, retrieved on 2023-02-19, to hygraph.com
tutorial here:
https://hygraph.com/blog/routing-in-react

This code is modified from a tutorial video about React Router V6 from Dennis Ivy on 2022-06-02, retrieved on 2023-02-19, to youtube.com
tutorial video here:
https://www.youtube.com/watch?v=2k8NleFjG7I
*/

import React from 'react';
import { Outlet } from 'react-router-dom';
import Grid from '@mui/material/Grid';

import Navbar from './components/Navbar/Navbar';
import './App.css'

const App = () => {
    return (
    <Grid container>
        <Navbar />
        <Outlet />
    </Grid>
    );
};

export default App;
