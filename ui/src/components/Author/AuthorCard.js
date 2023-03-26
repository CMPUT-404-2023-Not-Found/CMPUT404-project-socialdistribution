import React, { useContext }from "react";
import { CardContent, CardHeader, IconButton, Typography } from '@mui/material';
import GitHubIcon from '@mui/icons-material/GitHub';
import ToolTip from '@mui/material/Tooltip';

import BasicCard from '../common/BasicCard/BasicCard';
import BasicAvatar from '../common/BasicAvatar/BasicAvatar';
import AuthContext from '../../context/AuthContext';
import Backend from '../../utils/Backend';


const AuthorCard = ({ children, author, size }) => {
  const { user, authTokens, logoutUser } = useContext(AuthContext);
  
  // Should I be dealing witht the onclick event in this file or in Followers.js?
  // Have to implement delete in Backend.js
  const deleteFollower = async () => {
    const [response, data] = await Backend.get(`/api/authors/${user.user_id}/followers/`, authTokens.access);
    console.log("deleted");
  }

  return (
    <>
      <BasicCard>
        <CardHeader
          avatar={<BasicAvatar profile={author} size={size}></BasicAvatar>}
          title={author.displayName}
          titleTypographyProps={size === 'medium' ? { variant: "body1" } : {variant: "h3"}}
          subheader={author.host}
          subheaderTypographyProps={size === 'medium' ? { variant: "body1" } : {variant: "h4"}}
          action={
            <ToolTip title={author.github && author.github}>
              <IconButton
                size={size}
                aria-label="github"
                onClick={() => {
                  console.log(author.github);
                }}
              >
                <GitHubIcon fontSize={size} />
              </IconButton>
            </ToolTip>
          }
        />
        <CardContent>
          <Typography variant={size === 'medium' ? 'body1' : 'h5'}>ID</Typography>
          <Typography variant="body1">{author.url}</Typography>
        </CardContent>
        {children}
      </BasicCard>
    </>
  );
};

export default AuthorCard;
