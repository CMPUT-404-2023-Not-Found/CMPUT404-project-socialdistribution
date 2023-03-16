/*
2023-03-16
ui/src/components/Page/PageHeader.js

*/
import React from 'react';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';

import BasicAvatar from '../common/BasicAvatar/BasicAvatar';
import { pageStyles } from './styles';

const PageHeader = ({ title, profile }) => {
  return (
    <Box sx={pageStyles.PageHeader.wrapper}>
        <Box sx={pageStyles.PageHeader.topRow}>
            <BasicAvatar profile={profile} size='medium'></BasicAvatar>
        </Box>
        <Box sx={pageStyles.PageHeader.middleRow}>
            <Typography variant='h1' color='white'>{title}</Typography>
        </Box>
    </Box>
  );
}

export default PageHeader;
