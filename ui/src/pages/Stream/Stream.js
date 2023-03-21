/*
2023-03-13
ui/src/pages/Stream/Stream.js

*/

import React from 'react';
import { Typography } from '@mui/material';

import BasicCard from '../../components/common/BasicCard/BasicCard';
import GridWrapper from '../../components/common/GridWrapper/GridWrapper';
import PageHeader from '../../components/Page/PageHeader';

const Stream = () => {
    return (
        <>
            <PageHeader title='Stream'></PageHeader>
            <GridWrapper>
                <BasicCard header={<Typography>Header</Typography>} content={<Typography>Content</Typography>}></BasicCard>
            </GridWrapper>
        </>
    );
}

export default Stream;
