// From
// https://hygraph.com/blog/routing-in-react
// App.js

// login redirection
// https://www.youtube.com/watch?v=2k8NleFjG7I

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
    <>
       <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/" element={<Stream />} />
          <Route path="/createpost" element={<CreatePost />} />
          <Route path="/post" element={<Post />} />
          <Route path="/posts/:postid" element={<PostDetail />} />
          <Route path="*" element={<NoMatch />} />
       </Routes>
    </>
 );
};

export default App;