/*
2023-03-25
ui/src/components/Post/PostActions.js

*/

import React from 'react';
import { styled } from '@mui/material/styles';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import Collapse from '@mui/material/Collapse';
import Typography from '@mui/material/Typography';
import FavoriteIcon from '@mui/icons-material/Favorite';
import IconButton from '@mui/material/IconButton';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import List from '@mui/material/List';
import Divider from '@mui/material/Divider';
import SendIcon from '@mui/icons-material/Send';

import ShareAction from '../Actions/ShareAction/ShareAction';

import Comment from './Comment';
import BasicPagination from '../common/BasicPagination/BasicPagination';
import { parsePathFromURL } from '../../utils/Utils';
import { Box, Button, TextField } from '@mui/material';
import BasicAvatar from '../common/BasicAvatar/BasicAvatar';
import AuthContext from '../../context/AuthContext';
import Backend from '../../utils/Backend';
import { isValidHttpUrl, getInboxUrl } from '../../utils/Utils'

/*
This code is modified from a documentation guide on Material UI Card components from Material UI SAS 2023, retrieved 2023-03-13 from mui.com
guide here
https://mui.com/material-ui/react-card/#complex-interaction
*/
const ExpandMore = styled((props) => {
    const { expand, ...other } = props;
    return <IconButton {...other} />;
    })(({ theme, expand }) => ({
        transform: !expand ? 'rotate(0deg)' : 'rotate(180deg)',
        marginLeft: 'auto',
        transition: theme.transitions.create('transform', {
            duration: theme.transitions.duration.shortest,
    }),
}));

const PostActions = ({ disableLike=false, disableShare=false, disableComments=false, postNodeId }) => {    
    const [expanded, setExpanded] = React.useState(false);
    const [comments, setComments] = React.useState([]);
    const [commentText, setCommentText] = React.useState('');

    const [ showNotification, setShowNotification ] = React.useState(false);
    const [ notificationSeverity, setNotificationSeverity ] = React.useState('info');
    const [ notificationMessage, setNotificationMessage ] = React.useState('');

    const { user, authTokens, logoutUser } = React.useContext(AuthContext);
    const postPath = parsePathFromURL(postNodeId);
    const commentEndpoint = `${postPath}/comments`;
    const itemResultsKey = 'comments';

    const handleExpandClick = () => {
        setExpanded(!expanded);
    };

    const sendComment = async () => {
        const url = new URL(postNodeId);

        try {
            const [response, responseData] = await Backend.post(
                `${url.pathname}/comments/`, authTokens.access, JSON.stringify({
                    "comment" : commentText,
                    "contentType": "text/plain",
                })
            )

            if (response.status && response.status === 201) {
                setNotificationMessage('Comment Posted!');
                setNotificationSeverity('success');
                setShowNotification(true);
            } else if (response.statusText === 'Unauthorized'){
                // logoutUser();
            } else {
                console.log('Failed to send request');
                console.debug(response);
            }
        } catch (error) {
            console.log('Probably tried to comment on another node, ', error);
        }

        console.log(user);
        let inboxData = {
            summary: `${user.displayName} commented on your post`,
            type: 'comment',
            object: {
                url: `${postNodeId}/comments/`
            },
            inbox_urls : [getInboxUrl(`${user.url}`)]
        }
        const [ frResponse, frData ] = await Backend.post(`/api/node/object/`, authTokens.access, JSON.stringify(inboxData));
        if (frResponse.status && frResponse.status === 201) {
            setNotificationMessage('Follow request sent!');
            setNotificationSeverity('success');
            setShowNotification(true);
        } else if (frResponse.statusText === 'Unauthorized'){
            logoutUser();
        } else {
            console.log('Failed to send request');
            console.debug(frResponse);
        }
    }

    const renderComments = () => {
        if (!comments || comments.length <= 0) {
            return (
                <CardContent>
                    <Typography paragraph>
                        No comments
                    </Typography>
                </CardContent>
            );
        }
        let commentRender = [];
        comments.forEach((item, idx) => {
            console.debug(item);
            commentRender.push(
                <Comment key={idx * 2} comment={item}/>
            );
            if (idx < comments.length-1 ) { 
                commentRender.push(
                    <Divider key={idx * 2 + 1} variant="inset" component="li" />
                );
            }
        });
        return (
            <List>
                {commentRender}
            </List>
        );
    };

    return (<>
    <CardActions disableSpacing>
        {!disableLike && 
        <IconButton aria-label="like">
            <FavoriteIcon />
        </IconButton>
        }
        {!disableShare && <ShareAction objectNodeId={postNodeId}/>}
        {!disableComments &&
        <ExpandMore
            expand={expanded}
            onClick={handleExpandClick}
            aria-expanded={expanded}
            aria-label="show more"
        >
            <ExpandMoreIcon />
        </ExpandMore>
        }
    </CardActions>
    {/* This code is adapted from the Material UI docs, retrieved on 2023-03-26
    https://mui.com/material-ui/react-list/ */}
    {!disableComments && 
    <Collapse in={expanded} timeout="auto" unmountOnExit>
        <Box sx={{
            display: 'flex',
            alignItems: 'flex-start',
            paddingLeft: '20pt',
        }}>
            <BasicAvatar profile={user} size='small'></BasicAvatar>
            <TextField sx={{
                marginLeft: '10pt',
                width: '80%',
                marginRight: '10pt',
            }} value={commentText} variant='standard' placeholder='Add a comment ...' multiline onChange={
                (e) => {setCommentText(e.target.value)}
            }></TextField>
            <IconButton onClick={sendComment}>
                <SendIcon color='primary'></SendIcon>
            </IconButton>
            
        </Box>
        <CardContent>
            <BasicPagination 
                itemEndpoint={commentEndpoint} 
                itemResultsKey={itemResultsKey}
                setItems={(comments) => setComments(comments)}
            />
            <List>
            {renderComments()}
            </List>
        </CardContent>
    </Collapse>
    }
    </>);
}

export default PostActions;
