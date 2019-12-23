import React from 'react'

import { useSelector } from 'react-redux'
import PostComponent from './PostComponenet'
import { Loader } from 'components/Common/ContentLoader'

export const PostList = props => {
  const posts = useSelector(state => state.post.posts)
  console.log(posts)
  return (
    <Loader type="BlockUi" loadingRef="post.postLoading">
      { posts && posts.length ? posts.map((post) => <PostComponent key={post.id} post={post}></PostComponent>) : <></>}
    </Loader>
  )
}

export default PostList
