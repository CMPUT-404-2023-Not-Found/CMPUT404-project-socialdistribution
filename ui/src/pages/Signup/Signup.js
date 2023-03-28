/*
2023-03-27
pages/Signup/Signup.js
*/
import React, { useContext, useState } from 'react';
import Grid from '@mui/material/Grid';
import { useNavigate } from 'react-router-dom';
import { FaUser, FaUserCircle } from 'react-icons/fa';
import GppGoodIcon from '@mui/icons-material/GppGood';
import { RiLockPasswordFill } from 'react-icons/ri';
import { MdVisibility, MdVisibilityOff } from 'react-icons/md';
import styled from 'styled-components';
import Backend from '../../utils/Backend';

import AuthContext from '../../context/AuthContext';
import './Signup.css';

const Signup = () => {
  const [confirmPassword, setConfirmPassword] = useState('');
  const [username, setUsername] = useState('');
  
  const [password, setPassword] = useState('');
  const [usernameError, setUsernameError] = useState('');
  const [passwordError, setPasswordError] = useState('');
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const toggleShowPassword = () => setShowPassword(!showPassword);
  const toggleShowConfirmPassword = () => setShowConfirmPassword(!showConfirmPassword); 


  const Button = styled.button`
    background-color: #265156;
    color: white;
    font-size: 20px;
    padding: 5px 30px;
    border-radius: 20px;
    margin: 5px 40px;
    cursor: pointer;
    font-family: 'IM Fell English SC', serif;
  `;

  const handleUsernameChange = (e) => {
    const value = e.target.value;

    if (value.length <= 15) {
      setUsername(value);
      setUsernameError('');
    } else {
      setUsernameError('* invalid input');
    }
  };

  let navigate = useNavigate();
  let { registerUser } = useContext(AuthContext);

//   const handleSubmit = async (e) => {
//     e.preventDefault();
//     if (password !== confirmPassword) {
//         console.log(password, confirmPassword)
//       setPasswordError('Passwords do not match');
//     } else {
//       setPasswordError(''); // Clear password error state when passwords match
//       // Perform signup logic here and navigate to the appropriate page after successful signup
//     }
//   };

// const handleSubmit = async (e) => {
//     e.preventDefault();
//     if (password !== confirmPassword) {
//       setPasswordError('Passwords do not match');
//     } else {
//       setPasswordError(''); // Clear password error state when passwords match
//       try {
//         const response = await Backend.post('/api/authors/', JSON.stringify({
//           username: username,
//           password: password,
//         }));
//         if (response[0].ok) {
//           navigate('/login'); // Navigate to the login page after successful signup
//         } else {
//           console.log(response);
//           console.log(response[0].status);
//           console.error("Failed to create new author");
//         }
//       } catch (error) {
//         console.error("Error while creating new author");
//         console.error(error);
//       }
//     }
//   };

const handleSubmit = async (e) => {
    e.preventDefault();
    if (password !== confirmPassword) {
      setPasswordError('Passwords do not match');
    } else {
      setPasswordError('');
      try {
        const response = await fetch('/api/authors/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            username: username,
            password: password,
          }),
        });
        if (response.ok) {
          navigate('/login');
        } else {
          console.error("Failed to create new author");
        }
      } catch (error) {
        console.error("Error while creating new author");
        console.error(error);
      }
    }
  };
  
  
  

  return (
    <Grid item xs={12}>
      <div id="Signup">
        <div className="signup-style">
          <br />
          <div
            style={{
              display: 'flex',
              justifyContent: 'center',
              alignItems: 'center',
            }}
          >
            <FaUserCircle size={60} />
          </div>
          <h1 style={{ marginLeft: '10px' }}>Sign Up</h1>
          <form className="signup-form" onSubmit={handleSubmit}>
            <div className="input-container">
              <label htmlFor="username" className="icon-label">
                <FaUser />
              </label>
              <input
                type="text"
                id="username"
                name="username"
                placeholder="Username"
                data-testid="username-input"
                required
                style={{ height: 25, width: 170, borderRadius: '10px' }}
                onChange={handleUsernameChange}
              />
            </div>
            {usernameError && (
              <div style={{ color: 'red', textAlign: 'start' }}>
                {usernameError}
              </div>
            )}
            
            <br />
            <div className="input-container">
              <label htmlFor="password" className="icon-label">
                <RiLockPasswordFill />
              </label>
              <input
                id="password"
                type={showPassword ? 'text' : 'password'}
                placeholder="Password"
                required
                style={{ height: 25, width: 170, borderRadius: '10px' }}
                onChange={(e) => setPassword(e.target.value)}
              />
              <span onClick={toggleShowPassword} className="show-password-icon">
                {showPassword ? <MdVisibility /> : <MdVisibilityOff />}
              </span>
              <br />
            </div>

            <br />
            <br />
            <div className="input-container">
              <label htmlFor="confirmPassword" className="icon-label">
                <GppGoodIcon />
              </label>
              <input
                id="confirmPassword"
                type={showConfirmPassword ? 'text' : 'password'} // Use showConfirmPassword state
                placeholder="Confirm Password"
                required
                style={{ height: 25, width: 170, borderRadius: '10px' }}
                onChange={(e) => setConfirmPassword(e.target.value)}
              />
              <span onClick={toggleShowConfirmPassword} className="show-password-icon"> 
                {showConfirmPassword ? <MdVisibility /> : <MdVisibilityOff />}
              </span>
              <br />
            </div>
            {passwordError && (
            <div style={{ color: 'red', textAlign: 'start' }}>
                {passwordError}
            </div>
            )}
            <br />
            <Button type="submit">Sign Up</Button>
            <br />
          </form>
        </div>
      </div>
    </Grid>
  );
};

export default Signup;