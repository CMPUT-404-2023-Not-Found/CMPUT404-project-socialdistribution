import React from 'react';
import { useNavigate } from 'react-router-dom';

const NoMatch = () => {
    let navigate = useNavigate();

    return (
        <>
            <div>
                404 page not found
            </div>

            <button onClick={() => {
                navigate('/')
            }}>
                go back to stream
            </button>
        </>
    );
}

export default NoMatch;