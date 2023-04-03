/*
2023-03-26
ui/src/components/common/BasicPagination/BasicPagination.js

*/

import React, { useContext, useEffect, useState } from 'react';
import Box from '@mui/material/Box';
import Pagination from '@mui/material/Pagination';

import AuthContext from '../../../context/AuthContext';
import Backend from '../../../utils/Backend';

/*
This code is modified from a video tutorial on MUI pagination from Grepsoft on 2022-05-03, retrieved 2023-03-26 from youtube.com
video here:
https://youtu.be/37xPlDBaA4A
*/

const BasicPagination = ({ itemEndpoint, itemResultsKey, setItems }) => {
    //  variable declarations -------------------------------------
    const pageSize = 5;
    const [ pagination, setPagination ] = useState({
        count: 0,
        page: 1
    });
    const { authTokens, logoutUser } = useContext(AuthContext);

    //  event listeners -------------------------------------------
    useEffect(() => {
        const getItems = async () => {
            let pagination_endpoint = `${itemEndpoint}/?page=${pagination.page}&size=${pageSize}`;
            console.log(`Calling ${pagination_endpoint} for list of items...`);
            const [response, data] = await Backend.get(pagination_endpoint, authTokens.access);
            if (response.status && response.status === 200) {
                console.debug(data)
                console.log(data)
                setPagination(pagination => ({...pagination, count: data.count}));
                setItems(data[itemResultsKey]);
            } else if (response.statusText === 'Unauthorized'){
                logoutUser();
            } else {
                console.error(`Failed to get items from ${pagination_endpoint}`);
            }
        };
        getItems();
    }, [pagination.page, itemEndpoint, itemResultsKey, authTokens, logoutUser]);
    
    //  functions -------------------------------------------------
    const handlePageChange = (e, page) => {
        setPagination({ ...pagination, page: page});
    };

    // RENDER APP =================================================
    return (
        <Box 
            justifyContent='center' 
            alignItems='center' 
            display='flex'
            sx={{ margin: '20px 0px'}}
        >
            <Pagination
                color='primary'
                count={Math.ceil(pagination.count / pageSize)}
                onChange={handlePageChange}
            />
        </Box>
    );
}

export default BasicPagination;
