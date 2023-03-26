/*
2023-03-25
ui/src/components/Follow/FollowCard.js

*/
import React from 'react';
import { CardContent, CardHeader } from '@mui/material';
import Button from '@mui/material/Button';

import BasicCard from '../common/BasicCard/BasicCard';
import BasicAvatar from '../common/BasicAvatar/BasicAvatar';
import { followCardStyles } from './styles';

const FollowCard = ({ follow }) => {
    const onClickAccept = () => {
        console.log(`you accepted ${follow.actor.url} request`);
    };
    const onClickDecline = () => {
        console.log(`you declined ${follow.actor.url} request`);
    };

    return (
        <BasicCard>
            <CardHeader 
                title={follow.summary} 
                avatar={<BasicAvatar profile={follow.actor} size='medium'/>}
                titleTypographyProps={followCardStyles.cardHeader.titleTypographyProps}
            />
            <CardContent>
                <Button variant='contained' onClick={onClickAccept}>Accept</Button>
                <Button onClick={onClickDecline}>Decline</Button>
            </CardContent>
        </BasicCard>
    );
}

export default FollowCard;
