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

import ShareAction from '../Actions/ShareAction/ShareAction';

import Comment from './Comment';
import BasicPagination from '../common/BasicPagination/BasicPagination';
import { parsePathFromURL } from '../../utils/Utils';
import backend from '../../utils/Backend';


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
    const postPath = parsePathFromURL(postNodeId);
    const commentEndpoint = `${postPath}/comments`;
    const itemResultsKey = 'comments';

    const handleExpandClick = () => {
        setExpanded(!expanded);
    };
    // deal with like button
    const handleLike = async () => {
        setIsLiked(!isLiked);
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
