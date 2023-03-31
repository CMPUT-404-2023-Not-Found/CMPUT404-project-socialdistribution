/*
2023-03-25
ui/src/components/Post/PostActions.js

*/

import React from 'react';
import { styled } from '@mui/material/styles';
import Badge from '@mui/material/Badge';
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
import Chip from '@mui/material/Chip';
import Stack from '@mui/system/Stack';

import ShareAction from '../Actions/ShareAction/ShareAction';

import Comment from './Comment';
import BasicPagination from '../common/BasicPagination/BasicPagination';
import { parsePathFromURL } from '../../utils/Utils';
import { Box, TextField } from '@mui/material';
import BasicAvatar from '../common/BasicAvatar/BasicAvatar';
import AuthContext from '../../context/AuthContext';
import Backend from '../../utils/Backend';
import { getHostFromURL } from '../../utils/Utils';
import { postActionStyles } from './styles';

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

const PostActions = ({ disableLike=false, disableShare=false, disableComments=false, postNodeId, likeCount, commentCount, post, source='' }) => {    
    const [expanded, setExpanded] = React.useState(false);
    const [comments, setComments] = React.useState([]);
    const [commentText, setCommentText] = React.useState('');

    const { user, authTokens, logoutUser } = React.useContext(AuthContext);
    const postPath = parsePathFromURL(postNodeId);
    let commentEndpoint;
    let addComments = true;

    if (source.includes('node')) {
        addComments = false;
        commentEndpoint = `/api/node/${postNodeId}/comments`;
    } else {
        commentEndpoint = `${postPath}/comments`;
    }

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
                console.debug(responseData);
                setCommentText('');
                setComments([]); // to trigger the rerendering
            } else if (response.statusText === 'Unauthorized'){
                logoutUser();
            } else {
                console.log('Failed to send request');
                console.debug(response);
            }
        } catch (error) {
            // technically now the try catch is not needed but will still leave it in just in case
            console.log('Probably tried to comment on another node, ', error);
        }

        // removed sending comment to inbox
    }
    const renderChips = () => {
        const chips = [];
        if (post.origin) { chips.push(<Chip key={0} label={getHostFromURL(post.origin)} />); }
        if (['PUBLIC', 'FRIENDS'].includes(post.visibility)) {
            chips.push(<Chip key={1} label={post.visibility} color={postActionStyles.chips[post.visibility].color}/>); 
        }
        post.categories.forEach((category, idx)=>{
            chips.push(<Chip key={idx + 2} label={category}/>)
        });
        return chips;
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
            {likeCount ? 
                <Badge badgeContent={likeCount} color='error'>
                    <FavoriteIcon />
                </Badge>
            :
                <FavoriteIcon />
            }
        </IconButton>
        }
        {!disableShare && <ShareAction objectNodeId={postNodeId}/>}
        <Stack direction='row' spacing={1}>{renderChips()}</Stack>
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
        {   addComments && 
            <>
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
            </>
        }
            
        </Box>
        <CardContent>
            {/* adding key will trigger rerendering on a new comment being added */}
            <BasicPagination 
                key={comments}
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
