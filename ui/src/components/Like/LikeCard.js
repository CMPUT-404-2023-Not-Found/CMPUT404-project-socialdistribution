/*
2023-03-25
ui/src/components/Like/LikeCard.js

*/
import React from 'react';
import { CardContent, CardHeader } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import Button from '@mui/material/Button';

import BasicCard from '../common/BasicCard/BasicCard';
import BasicAvatar from '../common/BasicAvatar/BasicAvatar';
import { likeCardStyles } from './style';

const LikeCard = ({ like }) => {
    const navigate = useNavigate();

    return (
        <BasicCard>
            <CardHeader 
                title={like.summary} 
                avatar={<BasicAvatar profile={like.author} size='medium'/>}
                titleTypographyProps={likeCardStyles.cardHeader.titleTypographyProps}
            />
            <CardContent>
                <Button variant='contained' onClick={() => {navigate('/posts')}}>Go To Your Posts</Button>
            </CardContent>
        </BasicCard>
    );
}

export default LikeCard;
