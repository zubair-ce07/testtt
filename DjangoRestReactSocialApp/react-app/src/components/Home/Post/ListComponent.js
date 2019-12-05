import React from 'react'

import { useSelector } from 'react-redux'
import PostComponent from './PostComponenet'

export const PostList = props => {
  const posts = useSelector(state => state.post.posts)
  console.log(posts)
  return (
    posts.length ? posts.map((post) => <PostComponent key={post.id} post={post}></PostComponent>) : <></>
  )
}

export default PostList
