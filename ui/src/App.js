// From
// https://hygraph.com/blog/routing-in-react
// App.js

import { Routes, Route } from 'react-router-dom';
import CreatePost from './pages/CreatePost';
import Stream from './pages/Stream';
import Post from './pages/Post';

const App = () => {
 return (
    <>
       <Routes>
          <Route path="/" element={<Stream />} />
          <Route path="/createpost" element={<CreatePost />} />
          <Route path="/post" element={<Post />} />
       </Routes>
    </>
 );
};

export default App;