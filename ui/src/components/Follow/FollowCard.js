/*
2023-03-25
ui/src/components/Follow/FollowCard.js

*/
import React, { useEffect, useContext, useState } from 'react';
import { CardContent, CardHeader } from '@mui/material';
import Button from '@mui/material/Button';

import AuthContext from '../../context/AuthContext';
import Backend from '../../utils/Backend';
import BasicCard from '../common/BasicCard/BasicCard';
import BasicAvatar from '../common/BasicAvatar/BasicAvatar';
import { followCardStyles } from './styles';

const FollowCard = ({ follow }) => {
    const [ isFollower, setIsFollower ] = useState(false);
    const { user, authTokens, logoutUser } = useContext(AuthContext);

    useEffect(() => {
        const getFollower = async () => {
            const getFollowerEndpoint = `/api/authors/${user.user_id}/followers/${follow.actor.url}/`;
            console.debug(`Looking for exiting follower at ${getFollowerEndpoint}`);
            const [ response, data ] = await Backend.get(`${getFollowerEndpoint}`, authTokens.access);
            if (response.status && response.status === 200) {
                console.log(`Already follower at ${getFollowerEndpoint}`);
                console.debug(data);
                setIsFollower(true);
            } else if (response.statusText === 'Unauthorized'){
                logoutUser();
            } else {
                console.error(`Not follower at ${getFollowerEndpoint}`);
            }
        }
        getFollower();
    }, [ follow.actor.url, user, authTokens, logoutUser ])
    
    const onClickAccept = async () => {
        let acceptFollowEndpoint = `/api/authors/${user.user_id}/followers/${follow.actor.url}/`;
        console.debug(`Creating follower at ${acceptFollowEndpoint}`);
        const [ response, data ] = await Backend.put(`${acceptFollowEndpoint}`, authTokens.access);
        if (response.status && response.status === 201) {
            console.log('Created follower');
            console.debug(data);
            setIsFollower(true);
        } else if (response.statusText === 'Unauthorized'){
            logoutUser();
        } else {
            console.error(`Failed to create follower at [${acceptFollowEndpoint}]`);
        }
    };

    return (
        <BasicCard>
            <CardHeader 
                title={follow.summary} 
                avatar={<BasicAvatar profile={follow.actor} size='medium'/>}
                titleTypographyProps={followCardStyles.cardHeader.titleTypographyProps}
            />
            <CardContent>
                {isFollower ?
                    <Button variant='contained' disabled>Accepted</Button>
                : 
                    <Button variant='contained' onClick={onClickAccept}>Accept</Button>
                }
                
                {/* <Button disabled={disabled} onClick={onClickDecline}>Decline</Button> */}
            </CardContent>
        </BasicCard>
    );
}

export default FollowCard;
