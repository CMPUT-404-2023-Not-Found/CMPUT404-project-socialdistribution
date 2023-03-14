/*
2023-02-19
index.js
*/

import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import '@fontsource/roboto/300.css';
import '@fontsource/roboto/400.css';
import '@fontsource/roboto/500.css';
import '@fontsource/roboto/700.css';
import { ThemeProvider } from '@mui/material';

import App from './App';
import { appTheme } from './appTheme';
import { AuthProvider } from './context/AuthContext';
import PrivateRoutes from './utils/PrivateRoutes'
import Login from './pages/Login/Login';
import Profile from './pages/Profile';
import Stream from './pages/Stream/Stream';
import Posts from './pages/Posts';
import PostDetail from './components/PostDetail';
import NotFound from './components/NotFound';
import CreatePost from './pages/CreatePost';

import './index.css';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
   <ThemeProvider theme={appTheme}>
      <BrowserRouter>
         <AuthProvider>
            <Routes>
               <Route path='/' element={<App />}>
                  <Route element={<PrivateRoutes />}>
                     <Route path="/" element={<Stream/>} exact/>
                     <Route path="/posts" element={<Posts />} />
                     <Route path="/posts/:postid" element={<PostDetail />} />
                     <Route path="/profile" element={<Profile />} />
                     <Route path="/createpost" element={<CreatePost />} />
                  </Route>
                  <Route path="/login" element={<Login />} />
                  <Route path="*" element={<NotFound />} />
               </Route>
            </Routes>
         </AuthProvider>
      </BrowserRouter>
   </ThemeProvider>
);
