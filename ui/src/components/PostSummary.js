import React from 'react'
import { useNavigate } from 'react-router-dom';

const PostSummary = ({
        authorobject={},
        description="placeholder description",
        title="placehodler title",
        postid="dlfkajlkdjlkfja"
    }) => {
  
  const navigate = useNavigate();

  return (
    <>
        <button onClick={() => navigate(`posts/${postid}`)}>
          view in detail
        </button>
        <p>
            Title: {title} <br></br>
            This post was made by {authorobject.username} <br></br>
            The description is {description}
        </p>
    </>
  )
}

export default PostSummary;
