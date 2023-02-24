/*
2023-02-24
context/AuthContext.js

This code is modified from a tutorial video about React Router V6 from Dennis Ivy on 2022-06-02, retrieved on 2023-02-19, to youtube.com
tutorial video here:
https://www.youtube.com/watch?v=2k8NleFjG7I
*/

import { createContext, useState, useEffect } from "react";

const AuthContext = createContext();
export default AuthContext;

export const AuthProvider = ({children}) => {
    //  variable declarations -------------------------------------
    const [ authTokens, setAuthTokens ] = useState(null)
    const [ user, setUser ] = useState(null);

    //  event listners --------------------------------------------

    //  async functions -------------------------------------------
    const loginUser = async (e) =>  {
        e.preventDefault()
        let response = await fetch('http://localhost:8000/api/token/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({'username': e.target.username.value, 'password': e.target.password.value})
        })
        let data = await response.json()
        console.log('data ', data)
    }

    //  context ---------------------------------------------------
    let contextData = {
        loginUser: loginUser
    }

    // RENDER APP =================================================
    return (
        <AuthContext.Provider value={contextData}>
            {children}
        </AuthContext.Provider>
    )
}
