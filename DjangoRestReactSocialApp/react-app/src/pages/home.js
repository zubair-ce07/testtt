import React, { useEffect } from 'react'
import { useDispatch } from 'react-redux'
import AppLayout from '../layouts/AppLayout'
import ProfileComponent from 'components/Home/ProfileComponent'
import CreateUpdatePost from 'components/Home/Post/CreateUpdateComponent'
import PostList from 'components/Home/Post/ListComponent'

import { getPosts } from 'store/modules/post/post.action'

export const HomePage = props => {
  const dispatch = useDispatch()
  // Similar to componentDidMount and componentDidUpdate:
  useEffect(() => {
    dispatch(getPosts())
  })
  return (
    <div className="container-fluid gedf-wrapper">
      <div className="row">
        <div className="col-md-3">
          <ProfileComponent/>
        </div>
        <div className="col-md-6 gedf-main">

          <CreateUpdatePost mode={'create'}/>

          <PostList></PostList>
        </div>
      </div>
    </div>

  )
}
export default AppLayout(HomePage)
