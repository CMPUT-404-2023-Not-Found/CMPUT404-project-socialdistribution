/*
2023-02-24
utils/PrivateRoute.js

This code is modified from a tutorial video about Protected Routes in React Router V6 from Dennis Ivy on 2022-06-02, retrieved on 2023-02-24, to youtube.com
tutorial video here:
https://youtu.be/2k8NleFjG7I
*/
import { Outlet, Navigate } from 'react-router-dom'
import { useContext } from 'react'
import AuthContext from '../context/AuthContext'

const PrivateRoutes = () => {
    let {user} = useContext(AuthContext)

    return (
        user ? <Outlet/> : <Navigate to='/login'/>
    )
}

export default PrivateRoutes
