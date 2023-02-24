import React from 'react'
import { useNavigate } from 'react-router-dom';

const PostSummary = ({...data}) => {
  return (
    <div className='postSummary'>
        <h3>Title: {data.title}</h3>
        <h4>Author: {data.author.displayName}</h4>
        <h4>{data.description}</h4>
        <p>{data.content}</p>
        <a href={data.id + '/'}>View Details</a>
        <p>Comments: {data.commentCount}, Likes: {data.likeCount}</p>
        <p>Full payload</p>
        <p>
          {JSON.stringify(data)}
        </p>
    </div>
  )
}

export default PostSummary;
