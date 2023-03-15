/*
2023-03-13
ui/src/pages/Stream/Stream.js

*/

import React, { useContext, useEffect, useState } from 'react';
import { Typography } from '@mui/material';

import Backend from '../../utils/Backend';
import AuthContext from '../../context/AuthContext';
import BasicCard from '../../components/common/BasicCard/BasicCard';
import GridWrapper from '../../components/common/GridWrapper/GridWrapper';

const Stream = () => {
    //  variable declarations -------------------------------------
    const [ inbox, setInbox ] = useState({});
    const { user, authTokens, logoutUser } = useContext(AuthContext);
    
    //  event listners --------------------------------------------
    useEffect(() => {
        const getInbox = async () => {
            const [response, data] = await Backend.get(`/api/authors/${user.user_id}/inbox/`, authTokens.access);
            if (response.status && response.status === 200) {
                setInbox(data);
            } else if (response.statusText === 'Unauthorized'){
                logoutUser();
            } else {
                console.log('Failed to get posts');
            }
        };
        getInbox();
    }, [user, authTokens, logoutUser]);

    //  async functions -------------------------------------------

    // RENDER APP =================================================
    const renderInbox = (items) => {
        // console.log(items);
        if (!items || items.length <= 0) return (<Typography paragraph >No Posts</Typography>);
        let itemsRender = [];
        items.forEach((item, idx) => {
            switch(item.type) {
                case 'post':
                    console.log(item);
                    itemsRender.push(
                        <BasicCard key={idx} data={item}></BasicCard>
                    )
                    break;
                case 'comment':
                    // TODO render
                    break;
                case 'like':
                    // TODO render
                    break;
                case 'follow_request':
                    // TODO Render
                    break;
                default:
                    console.error('Unknown inbox type: ' + item.type);
            }
        });
        return (<>{itemsRender}</>)
    };

    return (
        <GridWrapper>
        {renderInbox(inbox.items)}
        </GridWrapper>
    );
}

export default Stream;
