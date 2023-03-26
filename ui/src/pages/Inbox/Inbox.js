/*
2023-03-13
ui/src/pages/Inbox/Inbox.js

*/

import React, { useContext, useEffect, useState } from 'react';
import Button from '@mui/material/Button';
import CardHeader from '@mui/material/CardHeader';
import CardContent from '@mui/material/CardContent';
import { useNavigate } from 'react-router-dom';

import Backend from '../../utils/Backend';
import AuthContext from '../../context/AuthContext';
import BasicCard from '../../components/common/BasicCard/BasicCard';
import PostCard from '../../components/Post/PostCard';
import GridWrapper from '../../components/common/GridWrapper/GridWrapper';
import PostHeader from '../../components/Post/PostHeader';
import PostContent from '../../components/Post/PostContent';
import PageHeader from '../../components/Page/PageHeader';
import LikeCard from '../../components/Like/LikeCard';

const Inbox = () => {
    //  variable declarations -------------------------------------
    const [ inbox, setInbox ] = useState({});
    const { user, authTokens, logoutUser } = useContext(AuthContext);
    const navigate = useNavigate();

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
        if (!items || items.length <= 0) {
            return (
            <BasicCard>
                <CardHeader title='No Posts' subheader='You have no notifications' />
                <CardContent>
                    <Button variant='contained' onClick={() => {navigate('/')}}>Go To Stream</Button>
                </CardContent>
            </BasicCard>);
        }
        let itemsRender = [];
        items.forEach((item, idx) => {
            console.log(item);
            let item_type = item.type.toLowerCase();
            switch(item_type) {
                case 'post':
                    itemsRender.push(<PostCard key={idx * 2} post={item} />);
                    break;
                case 'comment':
                    // TODO render
                    break;
                case 'like':
                    itemsRender.push(<LikeCard key={idx * 2} like={item}/>)
                    break;
                case 'follow':
                    // TODO Render
                    break;
                default:
                    console.error('Unknown inbox type: ' + item.type);
                    itemsRender.push(
                        <BasicCard 
                            key={idx * 2}
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
            }
            itemsRender.push(<br key={idx * 2 + 1}></br>);
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
