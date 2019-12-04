import React, { useEffect } from 'react'
import { useDispatch } from 'react-redux'
import AppLayout from '../layouts/AppLayout'
import ProfileComponent from 'components/Home/ProfileComponent'
import CreatePost from 'components/Home/CreatePostComponent'
import PostList from 'components/Home/PostListComponent'

import { getPosts } from 'store/modules/post/post.action'

export const HomePage = props => {
  const dispatch = useDispatch()
  // Similar to componentDidMount and componentDidUpdate:
  useEffect(() => {
    console.log('use effect called')
    // Update the document title using the browser API
    dispatch(getPosts())
  })
  return (
    <div className="container-fluid gedf-wrapper">
      <div className="row">
        <div className="col-md-3">
          <ProfileComponent/>
        </div>
        <div className="col-md-6 gedf-main">

          <CreatePost></CreatePost>

          <PostList></PostList>
        </div>
      </div>
    </div>

  )
}
export default AppLayout(HomePage)
