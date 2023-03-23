/*
2023-03-22
pages/Followers/Followers.js
*/
import React, { useContext, useEffect, useState } from 'react';
import { CardContent, CardHeader, IconButton, Typography } from '@mui/material';
import GitHubIcon from '@mui/icons-material/GitHub';
import ToolTip from '@mui/material/Tooltip';

import BasicAvatar from '../../components/common/BasicAvatar/BasicAvatar';
import BasicCard from '../../components/common/BasicCard/BasicCard';
import GridWrapper from '../../components/common/GridWrapper/GridWrapper';
import AuthContext from '../../context/AuthContext';
import Backend from '../../utils/Backend';
import PageHeader from '../../components/Page/PageHeader';

const Followers = () => {
    //  variable declarations -------------------------------------
    const [ followers, setFollowers ] = useState({});
    const { user, authTokens, logoutUser } = useContext(AuthContext);

    //  event listeners --------------------------------------------
    useEffect(() => {
        const getFollowers = async () => {
            const [response, data] = await Backend.get(`/api/authors/${user.user_id}/followers/`, authTokens.access);
            if (response.status && response.status === 200) {
                console.log('Got followers');
                console.log(data);
                setFollowers(data);
            } else if (response.statusText === 'Unauthorized'){
                logoutUser();
            } else {
                console.log('Failed to get followers');
            }
        };
        getFollowers();
    }, [ user, authTokens, logoutUser ]);

    // render functions ------------------------------------------
    const renderFollowers = (items) => {
        if (!items || items.length <= 0) return (<Typography paragraph >No Followers</Typography>);
        let itemsRender = [];
        items.forEach((item, idx) => {
            console.log(item);
            itemsRender.push(
                <BasicCard key ={idx}>
                <CardHeader
                    avatar={
                        <BasicAvatar profile={item} size='large'></BasicAvatar>
                    }
                    title={item.displayName}
                    titleTypographyProps={{ variant: 'h3' }}
                    subheader={item.host}
                    subheaderTypographyProps={{ variant: 'h4' }}
                    action={
                    <ToolTip title={(item.github && item.github)}>
                    <IconButton size='large' aria-label="github" onClick={() => { console.log(item.github) }}>
                        <GitHubIcon fontSize='large'/>
                    </IconButton>
                    </ToolTip>
                    }
                />
                <CardContent>
                    <Typography variant='h5'>ID</Typography>
                    <Typography variant='body1'>{item.url}</Typography>
                </CardContent>
            </BasicCard>
            );
            itemsRender.push(<br key={idx + items.length}></br>);
        });
        return (<>{itemsRender}</>)
    }
    // RENDER APP =================================================
    return (
    <>
        <PageHeader followers={followers} title='Followers'></PageHeader>
        <GridWrapper>
            {renderFollowers(followers.items)}
        </GridWrapper>
    </>
  )
}

export default Followers
