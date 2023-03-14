/*
2023-03-13
ui/src/componenets/Navbar/consts/styles.js

This code is modified from a video tutorial on Material UI from theatypicaldeveloper on 2021-11-29, retrieved 2023-03-13 from youtube.com
video here:
https://youtu.be/uLSE7WtcrP0
*/
export const navbarStyles = {
    drawer: {
        width: 320,
        flexShrink: 0,
        '& .MuiDrawer-paper': {
            width: 320,
            boxSizing: 'border-box',
            color: '#265156',
        },
        '& .Mui-selected': {
            color: 'red',
        },
    },
    icons: {
        color: '#265156!important',
        marginLeft: '20px',
    },
    text: {
        '& span': {
            marginLeft: '-10px',
            fontWeight: '500',
            fontSize: '16px',
        }
    }
};
