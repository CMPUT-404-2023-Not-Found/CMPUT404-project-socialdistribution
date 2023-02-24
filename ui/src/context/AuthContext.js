/*
2023-02-24
context/AuthContext.js

This code is modified from a tutorial video about React Router V6 from Dennis Ivy on 2022-06-02, retrieved on 2023-02-19, to youtube.com
tutorial video here:
https://www.youtube.com/watch?v=2k8NleFjG7I
*/

import { createContext, useState, useEffect } from "react";
import jwt_decode from 'jwt-decode'
import { useNavigate } from "react-router-dom";

const AuthContext = createContext();
export default AuthContext;

export const AuthProvider = ({children}) => {
    //  variable declarations -------------------------------------
    const [ authTokens, setAuthTokens ] = useState(() => localStorage.getItem('authTokens') ? JSON.parse(localStorage.getItem('authTokens')) : null);
    const [ user, setUser ] = useState(() => localStorage.getItem('authTokens') ? jwt_decode(localStorage.getItem('authTokens')) : null);
    const [ loading, setLoading ] = useState(true);
    const navigate = useNavigate();

    //  event listners --------------------------------------------
    useEffect(() => {
        // Refresh access token every 1 hour
        const oneHour = 60 * 60 * 1000;
        let interval = setInterval(() => {
            if (authTokens) {
                updateToken()
            }
        }, oneHour);
        return () => clearInterval(interval);
    }, [authTokens, loading])

    //  async functions -------------------------------------------
    const loginUser = async (e) =>  {
        e.preventDefault();
        let response = await fetch('http://localhost:8000/api/token/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({'username': e.target.username.value, 'password': e.target.password.value})
        });
        let data = await response.json()
        if (response.status && response.status == 200) {
            setAuthTokens(data);
            setUser(jwt_decode(data.access));
            localStorage.setItem('authTokens', JSON.stringify(data));
            navigate('/');
        } else {
            alert('Opps! Login failed.');
        }
    }

    const logoutUser = () => {
        setAuthTokens(null);
        setUser(null);
        localStorage.removeItem('authTokens');
        navigate('/login');
    }

    const updateToken = async () => {
        console.log('Updating');
        let response = await fetch('http://localhost:8000/api/token/refresh/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({'refresh': authTokens.refresh})
        });
        let data = await response.json();
        if (response.status && response.status == 200) {
            setAuthTokens(data);
            setUser(jwt_decode(data.access));
            localStorage.setItem('authTokens', JSON.stringify(data));
        } else {
            logoutUser();
        }
    }

    //  context ---------------------------------------------------
    let contextData = {
        user: user,
        loginUser: loginUser,
        logoutUser: logoutUser
    };

    // RENDER APP =================================================
    return (
        <AuthContext.Provider value={contextData}>
            {children}
        </AuthContext.Provider>
    );
}
