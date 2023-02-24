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
// General & Login pages
import Login from './pages/Login';
import Stream from './pages/Stream';
// Post pages
import CreatePost from './pages/CreatePost';
import Post from './pages/Post';
import PostDetail from './components/PostDetail';
// Error pages
import NoMatch from './components/NoMatch';

const App = () => {
    return (
    <div className='App'>
        <Routes>
            <Route path="/" element={<Stream/>} />
            <Route path="/login" element={<Login />} />

            <Route path="/createpost" element={<CreatePost />} />
            <Route path="/post" element={<Post />} />
            <Route path="/posts/:postid" element={<PostDetail />} />

            <Route path="*" element={<NoMatch />} />
        </Routes>
    </div>
    );
};

export default App;