/*
2023-03-13
ui/src/pages/Stream/Stream.js

*/

import React, { useContext, useEffect, useState } from 'react';
import Grid from "@mui/material/Grid";
import CommonCard from '../../components/common/commonCard/CommonCard';


import Backend from '../../utils/Backend';
import AuthContext from '../../context/AuthContext';
import { Typography } from '@mui/material';

const Stream = () => {
    //  variable declarations -------------------------------------
    const [ inbox, setInbox ] = useState({});
    const { user, authTokens, logoutUser } = useContext(AuthContext);
    
    //  event listners --------------------------------------------
    useEffect(() => {
        getInbox();
    }, []);

    //  async functions -------------------------------------------
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
                        <CommonCard key={idx} data={item}></CommonCard>
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
        <Grid item xs={8}>
        {renderInbox(inbox.items)}
        </Grid>
    );
}

export default Stream;
