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
    const [ followers, setFollowers ] = useState([]);
    const { user, authTokens, logoutUser } = useContext(AuthContext);

    //  event listeners --------------------------------------------
    useEffect(() => {
        const getFollowers = async () => {
            const [response, data] = await Backend.get(`/api/authors/${user.user_id}/followers/`, authTokens.access);
            if (response.status && response.status === 200) {
                console.log('Got followers');
                console.log(data);
                setFollowers(data.items);
            } else if (response.statusText === 'Unauthorized'){
                logoutUser();
            } else {
                console.log('Failed to get followers');
            }
        };
        getFollowers();
    }, [ user, authTokens, logoutUser ]);

    const deleteFollower = async (follower, idx) => {
        const response = await Backend.delete(`/api/authors/${user.user_id}/followers/${follower.id}`, authTokens.access);
        if (response.status && response.status === 204) {
            console.log("Deleted Follower");
            followers.splice(idx,1);
            setFollowers([...followers]);
        } else if (response.statusText === 'Unauthorized'){
            logoutUser();
        } else {
            console.log('Failed to delete follower');
        }
    }

    // render functions ------------------------------------------
    const renderFollowers = (followers) => {
        if (!followers || followers.length <= 0) return (<Typography paragraph >No Followers</Typography>);
        let itemsRender = [];
        followers.forEach((follower, idx) => {
            itemsRender.push(
                <AuthorCard author = {follower} size = "medium"> 
                    <div>
                        <IconButton 
                            aria-label="delete-follower"
                            onClick={()=> deleteFollower(follower, idx)}>
                        <PersonRemoveIcon/>
                        </IconButton>
                    </div>
                </AuthorCard>
            );
            itemsRender.push(<br key={idx + followers.length}></br>);
        });
        return (<>{itemsRender}</>)
    }
    // RENDER APP =================================================
    return (
    <>
        <PageHeader followers={followers} title='Followers'></PageHeader>
        <GridWrapper>
            {renderFollowers(followers)}
        </GridWrapper>
    </>
  )
}

export default Followers
