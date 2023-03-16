/*
2023-03-15
ui/src/components/common/Avatar/Avatar.js

*/
import React from 'react'
import Avatar from '@mui/material/Avatar';

import { avatarStyles } from './styles';

const BasicAvatar = ({ profile, size }) => {
    const authorName = profile.displayName;
    const authorNameShort = (authorName ? authorName.charAt(0) : 'h');
    const avatarSize = (size ? size : 'small');
    if (profile.profileImage) {
        return (
        <Avatar alt={authorName} src={profile.profileImage} sx={avatarStyles[avatarSize]}></Avatar>
        );
    } else {
        return (
        <Avatar sx={avatarStyles[avatarSize]}>{authorNameShort}</Avatar>
        );
    }
}

export default BasicAvatar;
