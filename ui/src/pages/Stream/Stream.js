/*
2023-03-13
ui/src/pages/Stream/Stream.js

*/

import React, { useContext, useEffect, useState } from 'react';
import { Typography, InputLabel, Select, MenuItem, FormControl } from '@mui/material';

import Backend from '../../utils/Backend';
import AuthContext from '../../context/AuthContext';
import GridWrapper from '../../components/common/GridWrapper/GridWrapper';
import PostCard from '../../components/Post/PostCard';
import PageHeader from '../../components/Page/PageHeader';

const Stream = () => {
    //  variable declarations -------------------------------------
    const [ nodePosts, setNodePosts ] = useState({});
    const { authTokens, logoutUser } = useContext(AuthContext);
    const [nodeURL, setNodeURL] = useState('Home');
    const [nodes, setNodes] = useState({});

    //  event listners --------------------------------------------
    useEffect(() => {
        const getNodePosts = async () => {
            const [response, data] = await Backend.get(`/api/posts/`, authTokens.access);
            if (response.status && response.status === 200) {
                console.log(data)
                setNodePosts(data);
            } else if (response.statusText === 'Unauthorized'){
                logoutUser();
            } else {
                console.log('Failed to get posts');
            }
        };

        const getNodes = async () => {
            const [response, data] = await Backend.get(`/api/node/`, authTokens.access);
            if (response.status && response.status === 200) {
                console.log(data)
                setNodes(data);
            } else if (response.statusText === 'Unauthorized'){
                logoutUser();
            } else {
                console.log('Failed to get posts');
            }    
        }
        getNodePosts();
        getNodes();
    }, [authTokens, logoutUser]);

    const handleNodeURLSelect = (event) => {
        let prevURL = nodeURL;
        setNodeURL(event.target.value);

        if (nodeURL != prevURL && nodeURL != 'Home') {
            // make backend call
        }
    }

    // RENDER APP =================================================
    const renderNodePosts = (items) => {
        if (!items || items.length <= 0) return (<Typography paragraph >No Posts</Typography>);
        let itemsRender = [];
        items.forEach((item, idx) => {
            console.log(item);
            itemsRender.push(<PostCard key={idx * 2} post={item} />);
            itemsRender.push(<br key={idx * 2 + 1} />);
        });
        return (<>{itemsRender}</>)
    };
    return (
        <>
            <PageHeader title='Stream'></PageHeader>

            <FormControl sx={{
                marginTop: 5,
                marginLeft: 40,
                width: '100%'
            }}>
                <InputLabel id="select-node-label">Node</InputLabel>
                <Select
                    labelId="select-node-label"
                    id="select-node"
                    value={nodeURL}
                    label="Node"
                    onChange={handleNodeURLSelect}
                >
                    <MenuItem value="Home">{nodeURL}</MenuItem>
                    { nodes.items ? nodes.items.map((item) => {
                        let url = `${item.host}${item.api_path}`
                        return (
                            <MenuItem value={url}>{item.host}</MenuItem>
                        )
                    }): null
                    }
                </Select>
            </FormControl>
            <GridWrapper>
            {renderNodePosts(nodePosts.items)}
            </GridWrapper>
        </>
    );
}

export default Stream;
