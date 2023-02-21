import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom';

const Login = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    let navigate = useNavigate();

    const login = () => {
        console.log(username);
        console.log(password);

        navigate(-1);
    }

    return (
        <div>
        placeholder for login

        <form action="" method="post">
            <label htmlFor="username">Username:</label>
            <input type="text" id="username" name="post_username" onChange={(e) => setUsername(e.target.value)}/>
            <br></br>

            <label htmlFor="password">Password:</label>
            <input type="password" id="password" name="post_password" onChange={(e) => setPassword(e.target.value)} />
            <br></br>

            <button type="button" onClick={login}>Send your message</button>
            <br></br>
        </form>

        </div>
    )
}

export default Login
