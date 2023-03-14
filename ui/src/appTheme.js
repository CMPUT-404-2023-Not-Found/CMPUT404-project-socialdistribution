import { createTheme } from '@mui/material/styles';

export const appTheme = createTheme({
    palette: {
        mode: 'light',
        primary: {
          main: '#265156',
        },
        secondary: {
          main: '#562651',
        },
        background: {
          default: '#efefef',
        },
      },
      typography: {
        fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
      },
});
