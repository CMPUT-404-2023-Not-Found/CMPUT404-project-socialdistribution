/*
2023-03-14
ui/src/components/common/commonCard/CommonCard.js
*/
import * as React from 'react';
import Card from '@mui/material/Card';
// import CardMedia from '@mui/material/CardMedia';

export default function BasicCard({ header, content }) { 
    return (
      <Card>
        {header}
        {content}
      </Card>
    );
}
