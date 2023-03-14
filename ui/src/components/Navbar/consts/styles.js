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
