/*
2023-03-13
ui/src/pages/Stream/Stream.js

*/

import React, { useContext, useEffect, useState } from 'react';
import { Typography, InputLabel, Select, MenuItem, FormControl } from '@mui/material';

import BasicPagination from '../../components/common/BasicPagination/BasicPagination';
import GridWrapper from '../../components/common/GridWrapper/GridWrapper';
import PostCard from '../../components/Post/PostCard';
import PageHeader from '../../components/Page/PageHeader';
import AuthContext from '../../context/AuthContext';
import Backend from '../../utils/Backend';

const Stream = () => {
    //  variable declarations -------------------------------------
    const itemResultsKey = 'items';
    const [ nodePosts, setNodePosts ] = useState([]);
    const { authTokens, logoutUser } = useContext(AuthContext);
    const [nodeURL, setNodeURL] = useState('/api/posts');
    const [nodes, setNodes] = useState({});

    //  event listners --------------------------------------------
    useEffect(() => {
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
        getNodes();
    }, []);

    const handleNodeURLSelect = async (event) => {
        setNodeURL(event.target.value);
        console.log("set it to, ", event.target.value)
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
                    <MenuItem value="/api/posts">Home</MenuItem>
                    { nodes.items ? nodes.items.map((item, i) => {
                        let url = `/api/node/${item.host}`;
                        let name = item.display_name;
                        if (name === '' || !name) {
                            name = item.host;
                        }
                        return (
                            <MenuItem key={i} value={url}>{name}</MenuItem>
                        )
                    }): null
                    }
                </Select>
            </FormControl>
            <GridWrapper>
            <BasicPagination 
                itemEndpoint={nodeURL} 
                itemResultsKey={itemResultsKey} 
                setItems={(posts) => setNodePosts(posts)}
            />
            {renderNodePosts(nodePosts)}
            </GridWrapper>
        </>
    );
}

export default Stream;
