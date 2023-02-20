import React from 'react'

const PostSummary = ({
        authorUsername="placeholder name",
        description="placeholder description"
    }
    ) => {
  return (
    <>
        <p>
            Post id: {}
            This post was made by {authorUsername} <br></br>
            The description is {description}
        </p>
    </>
  )
}

export default PostSummary;
