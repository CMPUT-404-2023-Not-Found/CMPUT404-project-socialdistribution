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

import './App.css'

import { Routes, Route } from 'react-router-dom';
// Componenets
import Navbar from './components/Navbar';
// Utils
import PrivateRoutes from './utils/PrivateRoutes'
// Contexts
import { AuthProvider } from './context/AuthContext';
// General & Login pages
import Login from './pages/Login';
import Profile from './pages/Profile';
import Stream from './pages/Stream';
// Post pages
import Posts from './pages/Posts';
import PostDetail from './components/PostDetail';
// Error pages
import NotFound from './components/NotFound';
import CreatePost from './pages/CreatePost';

const App = () => {
    return (
    <div className='App'>
        <AuthProvider>
            <Navbar />
            <Routes>
                    <Route element={<PrivateRoutes />}>
                        <Route path="/" element={<Stream/>} exact/>
                        <Route path="/posts" element={<Posts />} />
                        <Route path="/posts/:postid" element={<PostDetail />} />
                        <Route path="/profile" element={<Profile />} />
                        <Route path="/createpost" element={<CreatePost />} />
                    </Route>
                    <Route path="/login" element={<Login />} />
                    <Route path="*" element={<NotFound />} />
            </Routes>
        </AuthProvider>
    </div>
    );
};

export default App;
