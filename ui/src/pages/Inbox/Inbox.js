/*
2023-03-13
ui/src/pages/Inbox/Inbox.js

*/

import React, { useContext, useState } from 'react';
import Button from '@mui/material/Button';
import CardHeader from '@mui/material/CardHeader';
import CardContent from '@mui/material/CardContent';
import { useNavigate } from 'react-router-dom';

import AuthContext from '../../context/AuthContext';
import Backend from '../../utils/Backend';
import BasicPagination from '../../components/common/BasicPagination/BasicPagination';
import BasicCard from '../../components/common/BasicCard/BasicCard';
import CommonButton from '../../components/common/CommonButton/CommonButton';
import PostCard from '../../components/Post/PostCard';
import GridWrapper from '../../components/common/GridWrapper/GridWrapper';
import PostHeader from '../../components/Post/PostHeader';
import PostContent from '../../components/Post/PostContent';
import PageHeader from '../../components/Page/PageHeader';
import LikeCard from '../../components/Like/LikeCard';
import FollowCard from '../../components/Follow/FollowCard';

const Inbox = () => {
    //  variable declarations -------------------------------------
    const [ inboxItems, setInboxItems ] = useState([]);
    const { user, authTokens, logoutUser } = useContext(AuthContext);
    const navigate = useNavigate();
    const inboxEndpoint = `/api/authors/${user.user_id}/inbox`;
    const itemResultsKey = 'items';

    const onClickClearInbox = async (e) => {
        e.preventDefault();
        console.debug('Clearning inbox ...');
        console.debug(inboxEndpoint);
        const response = await Backend.delete(inboxEndpoint, authTokens.access);
        if (response.status && response.status === 204) {
            console.info('Cleared inbox data ...');
            setInboxItems([]);
        } else if (response.statusText === 'Unauthorized'){
            logoutUser();
        } else {
            console.error('Failed to clear inbox data');
        }
    }

    // RENDER APP =================================================
    const renderInbox = () => {
        if (!inboxItems || inboxItems.length <= 0) {
            return (
            <BasicCard>
                <CardHeader title='No Posts' subheader='You have no notifications' />
                <CardContent>
                    <Button variant='contained' onClick={() => {navigate('/')}}>Go To Stream</Button>
                </CardContent>
            </BasicCard>);
        }
        let itemsRender = [];
        inboxItems.forEach((item, idx) => {
            console.log(item);
            let item_type = item.type ? item.type.toLowerCase() : '';
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
                    itemsRender.push(<FollowCard key={idx * 2} follow={item}/>)
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
            <CommonButton variant='contained' onClick={onClickClearInbox}>Clear Inbox</CommonButton>
            <BasicPagination 
                itemEndpoint={inboxEndpoint} 
                itemResultsKey={itemResultsKey} 
                setItems={(inboxItems) => setInboxItems(inboxItems)}
            />
            {renderInbox(inboxItems)}
            </GridWrapper>
        </>
    );
}

export default Inbox;
