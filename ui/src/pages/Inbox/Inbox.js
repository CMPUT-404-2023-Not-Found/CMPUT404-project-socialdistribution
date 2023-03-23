/*
2023-03-13
ui/src/pages/Inbox/Inbox.js

*/

import React, { useContext, useEffect, useState } from 'react';
import { Typography } from '@mui/material';

import Backend from '../../utils/Backend';
import AuthContext from '../../context/AuthContext';
import BasicCard from '../../components/common/BasicCard/BasicCard';
import GridWrapper from '../../components/common/GridWrapper/GridWrapper';
import PostHeader from '../../components/Post/PostHeader';
import PostContent from '../../components/Post/PostContent';
import PageHeader from '../../components/Page/PageHeader';

const Inbox = () => {
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
            console.log(item);
            if (item['@context']) {
                itemsRender.push(
                    <BasicCard 
                        key={idx}
                        header = {
                            <PostHeader 
                                author={{ displayName: item.author }}
                                title={item.summary}
                            />
                        }
                        content = {
                            <PostContent 
                                description='Got an activitystream'
                                contentType={item['@context']}
                                content={item.object}
                            />
                        }
                    />
                );
            } else {
                switch(item.type) {
                case 'post':
                    itemsRender.push(
                        <BasicCard 
                            key={idx}
                            header={
                                <PostHeader 
                                    author={item.author} 
                                    title={item.title} 
                                    time={(item.updated_at ? item.updated_at : item.published)} 
                                />}
                            content={
                                <PostContent 
                                    description={item.description}
                                    contentType={item.contentType}
                                    content={item.content}
                                />}
                        />
                    );
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
            }
            itemsRender.push(<br key={items.length + idx}></br>);
        });
        return (<>{itemsRender}</>)
    };

    return (
        <>
            <PageHeader title='Inbox' disableNotification></PageHeader>
            <GridWrapper>
            {renderInbox(inbox.items)}
            </GridWrapper>
        </>
    );
}

export default Inbox;
