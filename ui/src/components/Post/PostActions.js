/*
2023-03-25
ui/src/components/Post/PostActions.js

*/

import React, { useState } from 'react';
import { styled } from '@mui/material/styles';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import Collapse from '@mui/material/Collapse';
import Typography from '@mui/material/Typography';
import FavoriteIcon from '@mui/icons-material/Favorite';
import IconButton from '@mui/material/IconButton';
import ShareIcon from '@mui/icons-material/Share';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';

import ShareWithFollower from '../Modals/ShareWithFollower/ShareWithFollower';

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

const PostActions = ({ postNodeId }) => {
    const [ open, setOpen ] = useState(false);
    const [expanded, setExpanded] = React.useState(false);

    const onClickShare = () => {
        setOpen(true);
    };

    const handleExpandClick = () => {
        setExpanded(!expanded);
    };

    return (<>
    <CardActions disableSpacing>
        <IconButton aria-label="like">
            <FavoriteIcon />
        </IconButton>
        <IconButton aria-label="share" onClick={onClickShare}>
            <ShareIcon />
        </IconButton>
        <ShareWithFollower open={open} onClose={() => setOpen(false)} postNodeId={postNodeId} />
        <ExpandMore
            expand={expanded}
            onClick={handleExpandClick}
            aria-expanded={expanded}
            aria-label="show more"
        >
            <ExpandMoreIcon />
        </ExpandMore>
    </CardActions>
    <Collapse in={expanded} timeout="auto" unmountOnExit>
        <CardContent>
        <Typography paragraph>
            Comments Go Here
        </Typography>
        </CardContent>
    </Collapse>
    </>);
}

export default PostActions;
