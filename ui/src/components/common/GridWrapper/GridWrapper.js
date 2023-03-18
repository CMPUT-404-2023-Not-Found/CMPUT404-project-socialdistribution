/*
2023-03-14
ui/src/componenets/common/GridWrapper/GridWrapper.js

This code is from a github repo for materialUi-in-react from theatypicaldeveloper, last commit on 2022-01-01, retrieved 2023-03-14
github repo here:
https://github.com/theatypicaldeveloper/materialUi-in-react/blob/lesson-5-card-and-searchbar/src/components/common/GridWrapper/GridWrapper.js
*/

import React from 'react'
import Grid from '@mui/material/Grid';
import { gridWrapperStyles } from './styles';

const GridWrapper = ({ children }) => {

    return (
        <Grid item xs={12} sx={gridWrapperStyles}>
            {children}
        </Grid>
    )
}

export default GridWrapper
