/*
2023-03-25
ui/src/components/common/CommonButton/CommonButton.js

This code is modified from a github repo for materialUi-in-react from theatypicaldeveloper, last commit on 2022-01-01, retrieved 2023-03-25
github repo here:
https://github.com/theatypicaldeveloper/materialUi-in-react/blob/lesson-6-modals/src/components/common/CommonButton/CommonButton.js
*/


import React from 'react'
import Button from '@mui/material/Button';

const CommonButton = ({ children, color, disabled, size, sx, variant, onClick }) => {
    return (
        <Button
            color={color}
            disabled={disabled}
            size={size}
            sx={sx}
            variant={variant}
            onClick={onClick}
        >
            {children}
        </Button>
    )
}

export default CommonButton
