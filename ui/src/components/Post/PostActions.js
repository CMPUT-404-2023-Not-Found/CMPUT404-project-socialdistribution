/*
2023-03-25
ui/src/components/Post/PostActions.js

*/

import React, { useContext, useEffect } from 'react';
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

import ShareAction from '../Actions/ShareAction/ShareAction';

import Comment from './Comment';
import BasicPagination from '../common/BasicPagination/BasicPagination';
import { parsePathFromURL } from '../../utils/Utils';
import Backend from '../../utils/Backend';
import AuthContext from '../../context/AuthContext';



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
    const [isLiked, setIsLiked] = React.useState(false);
    const { user, authTokens, logoutUser } = useContext(AuthContext);
    const postPath = parsePathFromURL(postNodeId);
    const commentEndpoint = `${postPath}/comments`;
    const itemResultsKey = 'comments';

    const handleExpandClick = () => {
        setExpanded(!expanded);
    };

    const handleLike = async () => {
        setIsLiked(!isLiked);
        if (!isLiked) {
            createLike(postNodeId);
        }
    };

    // ${postPath}/likes/ maybe the error?
    // object: postNodeId, -> backend cannot process this field always null
    // even Like created, still not showing in backend

    // TODO: fix this
    // TODO: fetch likes from backend and check if user has liked this post or not (set color to show the like status)
    // TODO: if user has liked this post, then when user click the like button, it should unlike the post (delete the like object from backend)
    
    const createLike = async (postNodeId) => {
        try {
          const response = await Backend.post(`${postPath}/likes/`,
            authTokens.access,
            JSON.stringify({
                summary: user.username + " like this post",
                author: "http://localhost:8000/api/authors/"+ user.user_id,
                object: postNodeId,
                "@context": "https://www.w3.org/ns/activitystreams" 
            })
          );
          const [resp, data] = response;
          console.log('PostNodeID ', postNodeId);
          console.log('Like created: ', data);
        } catch (error) {
          console.error('Error creating like: ', error);
        }
      };

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
        <IconButton aria-label="like" onClick={handleLike}>
            <FavoriteIcon style={{ color: isLiked ? '#CC0000' : 'inherit' }} />
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
