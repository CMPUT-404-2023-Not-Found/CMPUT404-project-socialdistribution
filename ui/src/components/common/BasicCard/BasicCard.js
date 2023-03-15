/*
2023-03-14
ui/src/components/common/commonCard/CommonCard.js

This code is modified from a documentation guide on Material UI Card components from Material UI SAS 2023, retrieved 2023-03-13 from mui.com
guide here
https://mui.com/material-ui/react-card/#complex-interaction
*/
import * as React from 'react';
import { styled } from '@mui/material/styles';
import Card from '@mui/material/Card';
import CardHeader from '@mui/material/CardHeader';
import CardMedia from '@mui/material/CardMedia';
import CardContent from '@mui/material/CardContent';
import CardActions from '@mui/material/CardActions';
import Collapse from '@mui/material/Collapse';
import Avatar from '@mui/material/Avatar';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import FavoriteIcon from '@mui/icons-material/Favorite';
import ShareIcon from '@mui/icons-material/Share';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import MoreVertIcon from '@mui/icons-material/MoreVert';

import { utcToLocal } from '../../../utils/Utils';

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

export default function CommonCard({ data }) {
    const [expanded, setExpanded] = React.useState(false);
  
    const handleExpandClick = () => {
      setExpanded(!expanded);
    };
    
    const renderAvatar = (author) => {
      let authorName = (author.displayName ? author.displayName : author.username);
      let authorNameShort = authorName.charAt(0);
      if (author.profileImage) {
        return (
          <Avatar alt={authorName} src={author.profileImage}>foobar</Avatar>
        )
      } else {
        return (
          <Avatar sx={{ bgcolor: 'primary.main' }}>{authorNameShort}</Avatar>
        )
      }
    }
    return (
      <Card>
        <CardHeader
          avatar={renderAvatar(data.author)}
          action={
            <IconButton aria-label="settings">
              <MoreVertIcon />
            </IconButton>
          }
          title={data.title}
          subheader={(data.updated_at > data.published ? utcToLocal(data.published) : utcToLocal(data.updated_at))}
        />
        <CardContent>
          <Typography variant="body2" color="text.secondary">
            {data.description}
          </Typography>
        </CardContent>
        <CardActions disableSpacing>
          <IconButton aria-label="add to favorites">
            <FavoriteIcon />
          </IconButton>
          <IconButton aria-label="share">
            <ShareIcon />
          </IconButton>
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
              {data.content}
            </Typography>
          </CardContent>
        </Collapse>
      </Card>
    );
}
