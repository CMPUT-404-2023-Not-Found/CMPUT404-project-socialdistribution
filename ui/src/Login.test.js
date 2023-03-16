import React from "react";
import {fireEvent, render, getByRole,getByLabelText,screen, getByTestId,queryByTestId,queryByDisplayValue,getByPlaceholderText } from '@testing-library/react'
import { AuthContext } from './context/AuthContext.js';
import { AuthProvider } from './context/AuthContext';
import Login from './pages/Login/Login';
import { act } from "react-dom/test-utils";

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
    renderWithAuth(<Login />)
);
});

// test('renders login form with username and password inputs', () => {
// const loginUserMock = jest.fn();
// render(
//     <AuthProvider value={{ loginUser: loginUserMock }}>
//     <Login />
//     </AuthProvider>
//     );
// });

// test('renders login form with username and password inputs', () => {
//     const loginUserMock = jest.fn();
//     const { getByPlaceholderText } = render(
//       <AuthProvider value={{ loginUser: loginUserMock }}>
//         <Login />
//       </AuthProvider>
//     );
  
//     const usernameInput = getByPlaceholderText('Username');
//     const passwordInput = getByPlaceholderText('Password');
  
//     expect(usernameInput).toBeInTheDocument();
//     expect(passwordInput).toBeInTheDocument();
//   });
  
// test('renders login form with username input', () => {
//   render(
//     <AuthProvider value={{ loginUser: jest.fn() }}>
//       <Login />
//     </AuthProvider>
//   );
  
//   const usernameInput = getByRole("textbox", { name: /Username/i });
//   expect(usernameInput).toBeInTheDocument();
// });

// test('renders login form with username input', () => {
//   const { getByRole } = render(
//     <AuthProvider value={{ loginUser: jest.fn() }}>
//       <Login />
//     </AuthProvider>
//   );
//   console.log("xxxxxxxxxx")
  
//   const usernameInput = screen.queryByTestId("username-input")
//   expect(usernameInput).toBeInTheDocument();

//   // const usernameInput = getByPlaceholderText<HTMLInputElement>(' Username');
//   // expect(usernameInput.name).toBe('username')
// });

// describe('Login', ()=>{
//     describe('invalid username', ()=>{
//         it('call the onSubmit function', async() => {
//             const mockOnSubmit = jest.fn()
//             const {getByPlaceHolderText, getByRole} = render(<Login onSubmit = {mockOnSubmit}/>)

//             await act(async () => {
//                 fireEvent.change(getByPlaceHolderText(' Username'), {target: {value: "xxxxxxxxxxxxx"}})
//                 fireEvent.change(getByPlaceHolderText(' Password'), {target: {value: "123456"}})
//             })

//             await act(async () => {
//                 fireEvent.click(getByRole('Button'))
//             })

//             expect(mockOnSubmit).toHaveBeenCalled()
//         })
//     })
// })

