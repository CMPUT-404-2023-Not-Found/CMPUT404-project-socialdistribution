/*
2023-03-25
ui/src/components/common/BasicModal/styles.js

This code is modified from a github repo for materialUi-in-react from theatypicaldeveloper, last commit on 2022-01-01, retrieved 2023-03-25
github repo here:
https://github.com/theatypicaldeveloper/materialUi-in-react/blob/lesson-6-modals/src/components/common/BasicModal/styles.js
*/

export const modalStyles = {
    wrapper: {
        position: 'absolute',
        top: '50%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
        width: 300,
        bgcolor: 'background.paper',
        boxShadow: 24,
        p: 4,
    },
    inputFields: {
        display: 'flex',
        flexDirection: 'column',
        marginTop: '20px',
        marginBottom: '15px',
        '.MuiInput-root': {
            marginBottom: '20px',
        },
    },
    buttons: {
        display: 'flex',
        justifyContent: 'end',
    }
};

