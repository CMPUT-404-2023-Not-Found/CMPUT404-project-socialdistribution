// From
// https://hygraph.com/blog/routing-in-react
// App.js

// login redirection
// https://www.youtube.com/watch?v=2k8NleFjG7I

import { Routes, Route } from 'react-router-dom';
import CreatePost from './pages/CreatePost';
import Stream from './pages/Stream';
import Post from './pages/Post';
import NoMatch from './components/NoMatch';
import PostDetail from './components/PostDetail';
import Login from './pages/Login';

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