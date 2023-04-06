
import React from "react";
import {fireEvent, render, getByRole,getByLabelText,screen, getByTestId,queryByTestId,queryByDisplayValue,getByPlaceholderText } from '@testing-library/react'
import { AuthContext } from '../context/AuthContext.js';
import { AuthProvider } from '../context/AuthContext.js';
import { act } from "react-dom/test-utils";
import Followers from "../pages/Followers/Followers.js";

// TODO: get these tests working 
// https://blog.logrocket.com/testing-react-router-usenavigate-hook-react-testing-library/

const mockedUsedNavigate = jest.fn();
jest.mock('react-router-dom', () => ({
   ...jest.requireActual('react-router-dom'),
  useNavigate: () => mockedUsedNavigate,
}));

// create a mock AuthContext provider
const mockAuthContext = {
    loginUser: jest.fn(),
    // add any other methods or properties your component depends on
  };
  
const renderWithAuth = (component) => {
return (
    <AuthProvider value={mockAuthContext}>
    {component}
    </AuthProvider>
    );
};
  
test('renders login component', () => {
const { getByTestId } = render(
    renderWithAuth(<Followers />)
);
});