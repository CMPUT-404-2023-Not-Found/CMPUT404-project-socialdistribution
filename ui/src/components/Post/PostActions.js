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
import AuthContext from '../../context/AuthContext';
import Backend from '../../utils/Backend';
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
    const { authTokens, logoutUser } = React.useContext(AuthContext);
    const [comments, setComments] = React.useState([]);

    //  event listners --------------------------------------------
    React.useEffect(() => {
        const getComments = async () => {
            const [response, data] = await Backend.getDirect(`${postNodeId}/comments`, authTokens.access);
            if (response.status && response.status === 200) {
                console.log(data)
                setComments(data.comments);
            } else if (response.statusText === 'Unauthorized'){
                logoutUser();
            } else {
                console.log('Failed to get posts');
            }
        };
        getComments();
    }, [authTokens, logoutUser]);

    const handleExpandClick = () => {
        setExpanded(!expanded);
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
        {comments.length > 0 ? 
            <List>
                <CardContent>
                {comments.map((comment, i) => {
                    return(
                       <React.Fragment key={i}>
                            <CardContent>
                                <Comment comment={comment}/>
                            </CardContent>
                            {i < comments.length-1 ? <Divider variant="inset" component="li" /> : null}
                        </React.Fragment>
                    )
                })}
                </CardContent>
            </List>
        : 
            <CardContent>
                <Typography paragraph>
                    No comments
                </Typography>
            </CardContent>
        }
    </Collapse>
    }
    </>);
}

export default PostActions;
