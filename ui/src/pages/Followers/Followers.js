/*
2023-03-22
pages/Followers/Followers.js
*/
import React, { useContext, useEffect, useState } from 'react';
import { Typography, IconButton } from '@mui/material';
import PersonRemoveIcon from '@mui/icons-material/PersonRemove';

import GridWrapper from '../../components/common/GridWrapper/GridWrapper';
import AuthContext from '../../context/AuthContext';
import Backend from '../../utils/Backend';
import PageHeader from '../../components/Page/PageHeader';
import AuthorCard from '../../components/Author/AuthorCard';

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

    const deleteFollower = async (author) => {
        const response = await Backend.delete(`/api/authors/${user.user_id}/followers/${author.id}`, authTokens.access);
        if (response.status && response.status === 204) {
            console.log("Deleted Follower");
        } else if (response.statusText === 'Unauthorized'){
            logoutUser();
        } else {
            console.log('Failed to delete follower');
        }
        // reloads window using the cached version of the page
        // seems sketch? better way to do this? 
        window.location.reload(false);
    }

    // render functions ------------------------------------------
    const renderFollowers = (items) => {
        if (!items || items.length <= 0) return (<Typography paragraph >No Followers</Typography>);
        let itemsRender = [];
        items.forEach((item, idx) => {
            itemsRender.push(
                <AuthorCard author = {item} size = "medium"> 
                    <div>
                        <IconButton 
                            aria-label="delete-follower"
                            onClick={()=> deleteFollower(item)}>
                        <PersonRemoveIcon/>
                        </IconButton>
                    </div>
                </AuthorCard>
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
