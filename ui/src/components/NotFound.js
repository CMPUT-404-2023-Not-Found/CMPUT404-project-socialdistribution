/*
2023-02-20
ui/src/components/NotFound.js

*/

import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Button, CardContent, CardHeader, Typography } from '@mui/material';

import BasicCard from '../components/common/BasicCard/BasicCard';
import GridWrapper from './common/GridWrapper/GridWrapper';

const NoMatch = () => {
    let navigate = useNavigate();
    return (
        <GridWrapper>
            <BasicCard
                header={<CardHeader title='404' subheader='Page Not Found' />}
                content={
                    <CardContent>
                        <Button variant='contained' onClick={() => {navigate('/')}}>Go Back To Stream</Button>
                    </CardContent>
                }
            />
        </GridWrapper>
    );
}

export default NoMatch;
