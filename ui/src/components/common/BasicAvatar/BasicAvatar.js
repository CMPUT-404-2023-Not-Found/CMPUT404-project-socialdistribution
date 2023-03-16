/*
2023-03-15
ui/src/components/common/Avatar/Avatar.js

*/
import React from 'react'
import Avatar from '@mui/material/Avatar';

const BasicAvatar = ({ profile }) => {
    const authorName = profile.displayName;
    const authorNameShort = authorName.charAt(0);
    if (profile.profileImage) {
        return (
        <Avatar alt={authorName} src={profile.profileImage} sx={{ width: 128, height: 128 }}></Avatar>
        );
    } else {
        return (
        <Avatar sx={{ bgcolor: 'primary.main', width: 128, height: 128 }}>{authorNameShort}</Avatar>
        );
    }
}

export default BasicAvatar;
