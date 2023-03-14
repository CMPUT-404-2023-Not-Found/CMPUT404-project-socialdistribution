/*
2023-02-21
pages/Login.js
*/
import React, { useContext, useState } from 'react'
import Grid from '@mui/material/Grid';
import { useNavigate } from 'react-router-dom';
import { FaUser, FaUserCircle } from 'react-icons/fa';
import { RiLockPasswordFill } from 'react-icons/ri'
import { MdVisibility, MdVisibilityOff } from "react-icons/md";
import styled from 'styled-components';

import AuthContext from '../../context/AuthContext';
import "./Login.css"

const Login = () => {
    //  variable declarations -------------------------------------
    const [username, setUsername] = useState('');
    // const [password, setPassword] = useState('');
    const [usernameError, setUsernameError] = useState('');

    const [showPassword, setShowPassword] = useState(false);
    const toggleShowPassword = () => setShowPassword(!showPassword);
    const Button = styled.button`
        background-color: #265156;
        color: white;
        font-size: 20px;
        padding: 5px 30px;
        border-radius: 20px;
        margin: 5px 40px;
        cursor: pointer;
        font-family: 'IM Fell English SC', serif;
        `;
    
    // left for future use (add invalid input msg)
    const handleUsernameChange = (e) => {
        const value = e.target.value;
    
        if (value.length <= 15) {
        setUsername(value);
        setUsernameError('');
        } else {
        setUsernameError('* invalid input');
        }
    };

    //  event listeners --------------------------------------------
    let navigate = useNavigate();
    let {loginUser} = useContext(AuthContext)
    //  async functions -------------------------------------------
    // RENDER APP =================================================
    return (
        <Grid item xs={12}>
        <div id="Login">
            <div className="login-style">
            <br></br>
            <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
            <FaUserCircle size={60} />
            </div>
            <h1 style={{ marginLeft: '10px' }}>Login In</h1>
                <form className="login-form" onSubmit={loginUser}>
                    <div className="input-container">
                    <label htmlFor="username" className="icon-label"><FaUser/> </label>
                    <input 
                        type="text" 
                        id="username" 
                        name="username" 
                        placeholder=" Username" 
                        data-testid="username-input"
                        required
                        style={{height:25,width:170,borderRadius: '10px'}}
                        onChange={handleUsernameChange}
                        />
                    </div>
                    {usernameError && <div style={{ color: 'red',textAlign:"start" }}>{usernameError}</div>}
                    <br></br>

                    <div className="input-container">
                    <label htmlFor="password" className="icon-label"><RiLockPasswordFill/> </label>
                    <input 
                        id="password"
                        type={showPassword ? 'text' : 'password'}
                        placeholder=" Password"
                        required
                        style={{height:25,width:170,borderRadius: '10px'}}
                    />
                    <span onClick={toggleShowPassword} className="show-password-icon">
                    {showPassword ? <MdVisibility/> : <MdVisibilityOff />}
                    </span>
                    <br></br>
                    </div>

                    <br></br>
                    <div className="forgot">
                        <a href="#">Sign up</a>
                    </div>

                    <br></br>
                    <Button type="submit">Login</Button>
                    <br></br>
                </form>
            </div>
        </div>
        </Grid>
    )
}

export default Login
