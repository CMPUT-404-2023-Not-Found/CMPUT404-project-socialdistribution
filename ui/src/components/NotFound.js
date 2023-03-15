import React from 'react';
import { useNavigate } from 'react-router-dom';
import GridWrapper from './common/GridWrapper/GridWrapper';

const NoMatch = () => {
    let navigate = useNavigate();

    return (
        <GridWrapper>
            <div>
                404 page not found
            </div>

            <button onClick={() => {
                navigate('/')
            }}>
                go back to stream
            </button>
        </GridWrapper>
    );
}

export default NoMatch;
