/*
2023-03-15
ui/src/components/Post/PostContent.js

*/

import React, { useState } from 'react'
import { styled } from '@mui/material/styles';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Collapse from '@mui/material/Collapse';
import Divider from '@mui/material/Divider';
import Typography from '@mui/material/Typography';
import FavoriteIcon from '@mui/icons-material/Favorite';
import IconButton from '@mui/material/IconButton';
import ShareIcon from '@mui/icons-material/Share';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import ReactMarkdown from 'react-markdown'

import BasicModal from '../../components/common/BasicModal/BasicModal';
import { PostContentStyles } from './styles';

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

const PostContent = ({ description, contentType, content }) => {
    const [ open, setOpen ] = useState(false);
    const [expanded, setExpanded] = React.useState(false);

    const onClickShare = () => {
        setOpen(true);
    };

    const handleExpandClick = () => {
        setExpanded(!expanded);
    };

    const renderContentBody = (description, contentType, content) => {
        let contentBodyRender = [];
        switch (contentType) {
            case 'text/plain': case 'application/base64': 
                contentBodyRender = 
                    <CardContent>
                        <Typography variant='body1' color='text.primary'>{content}</Typography>
                    </CardContent>
                break;
            case 'text/markdown':
                contentBodyRender = 
                    <CardContent>
                        <ReactMarkdown  components={{
                    img: ({node,...props})=><img style={{maxWidth:'400pt'}}{...props}/>}
                }>{content}</ReactMarkdown>
                    </CardContent>
                break;
            case 'image/png;base64': case 'image/jpeg;base64': case 'image/link':
                contentBodyRender = 
                    <CardMedia 
                        component='img' 
                        height={PostContentStyles.cardMedia.height} 
                        sx={PostContentStyles.cardMedia.sx}
                        src={content} alt={description} 
                        />
                break;
            case 'https://www.w3.org/ns/activitystreams':
                console.error('Got a raw activitystream for content: ', content);
                contentBodyRender =
                    <CardContent>
                        <Typography>Sorry, I wasn't able to get this notification.</Typography>
                    </CardContent>
                break;
            default:
                console.error('Got unknown contentType: ', contentType);
                contentBodyRender = 
                    <CardContent>
                        <Typography>Unable to render</Typography>
                    </CardContent>
                break;
        }
        return contentBodyRender;
    };

    return (<>
    <CardContent>
        <Typography variant="body2" color="text.secondary">
            {description}
        </Typography>
        <Divider light></Divider>
    </CardContent>
    {renderContentBody(description, contentType, content)}
    <CardActions disableSpacing>
        <IconButton aria-label="like">
        <FavoriteIcon />
        </IconButton>
        <IconButton aria-label="share" onClick={onClickShare}>
            <ShareIcon />
        </IconButton>
        <BasicModal open={open} onClose={() => setOpen(false)}></BasicModal>
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

export default PostContent
