import React, { useContext, useState } from 'react'
import { useNavigate } from 'react-router-dom';
import AuthContext from '../context/AuthContext';

const Login = () => {
    //  variable declarations -------------------------------------
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    let {loginUser} = useContext(AuthContext)

    //  event listners --------------------------------------------
    let navigate = useNavigate();

    //  async functions -------------------------------------------
    const login = () => {
        console.log(username);
        console.log(password);

        navigate(-1);
    }

    // RENDER APP =================================================
    return (
        <div>
        <h1>Login Page</h1>
        <form onSubmit={loginUser}>
            <label htmlFor="username">Username </label>
            <input 
                type="text" 
                id="username" 
                name="username" 
                placeholder="Type your username" 
                onChange={(e) => setUsername(e.target.value)}
                />
            <br></br>
            <label htmlFor="password">Password </label>
            <input 
                type="password" 
                id="password" 
                name="password" 
                placeholder="Type your username" 
                onChange={(e) => setPassword(e.target.value)} 
                />
            <br></br>
            <input type="submit" value="Login"/>
            <br></br>
        </form>

        </div>
    )
}

export default Login
