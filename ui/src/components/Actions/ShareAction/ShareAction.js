/*
2023-03-25
ui/src/components/Actions/ShareAction/ShareAction.js 

*/
import React, { useState } from 'react';
import IconButton from '@mui/material/IconButton';
import ShareIcon from '@mui/icons-material/Share';
import Tooltip from '@mui/material/Tooltip';

import ShareModal from '../../Modals/ShareModal/ShareModal'

const ShareAction = ({ objectNodeId }) => {
    const [ open, setOpen ] = useState(false);
    const onClickShare = () => {
        setOpen(true);
    };
    return (
        <>
        <Tooltip title='Share with your followers'>
        <IconButton aria-label="share" onClick={onClickShare}>
                <ShareIcon />
        </IconButton>
        </Tooltip>
        <ShareModal open={open} onClose={() => setOpen(false)} objectNodeId={objectNodeId} />
        </>
    );
}

export default ShareAction;
