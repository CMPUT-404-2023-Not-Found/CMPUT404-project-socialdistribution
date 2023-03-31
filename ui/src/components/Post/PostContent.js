/*
2023-03-15
ui/src/components/Post/PostContent.js

*/

import React from 'react'
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Divider from '@mui/material/Divider';
import Typography from '@mui/material/Typography';
import ReactMarkdown from 'react-markdown'

import { PostContentStyles } from './styles';

const PostContent = ({ description, contentType, content }) => {

    const renderContentBody = (description, contentType, content) => {
        let contentBodyRender;
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
                        <ReactMarkdown 
                            components={
                                { img: ({node,...props}) =>
                                    <img alt={description} style={{maxWidth:'400pt'}} {...props}/>
                                }}>
                            {content}
                        </ReactMarkdown>
                    </CardContent>
                break;
            case 'image/png;base64': case 'image/jpeg;base64': case 'image/link': case 'image/png': case 'image/jpeg':
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
    </>);
}

export default PostContent
