import React, { useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import PropTypes from 'prop-types'
import CommentsPanel from 'components/Home/Comment/ListComponent'

import { deletePost } from 'store/modules/post/post.action'

import { confirmBox, toast } from 'helpers/common'
import ActionComponent from 'components/Common/ActionComponent'
import CreatePost from './CreateUpdateComponent'
import PostView from './ViewComponent'

export const Post = ({ post }) => {
  const dispatch = useDispatch()
  const user = useSelector(state => state.user.user)

  const [mode, modeChange] = useState('view')

  const actionHandler = (type) => {
    if (type === 'delete') {
      confirmBox((result) => {
        dispatch(deletePost(post.id)).then((res) => {
          if (res.value.data.status) {
            toast('success', 'Post Deleted')
          } else {
            toast('success', 'Error while deleting post')
          }
        })
      })
    } else {
      modeChange('edit')
    }
  }
  return (

    <div className="card gedf-card">
      <div className="card-header">
        <div className="d-flex justify-content-between align-items-center">
          <div className="d-flex justify-content-between align-items-center">
            <div className="mr-2">
              <img className="rounded-circle" width="45" src="https://picsum.photos/50/50" alt="" />
            </div>
            <div className="ml-2">
              <div className="h5 m-0">@{post.author.username}</div>
              <div className="h7 text-muted">{post.author.first_name} {post.author.last_name}</div>
            </div>
          </div>
          <div>
            {user.id === post.author.id && <ActionComponent actionHandler={actionHandler}></ActionComponent>
            }
          </div>

        </div>

      </div>
      {
        mode === 'view' ? <PostView post={post}></PostView>
          : <CreatePost post={post} mode={'edit'} modeChange={modeChange}></CreatePost>
      }

      <CommentsPanel post={post} comments={post.comments}></CommentsPanel>
    </div>

  )
}

Post.propTypes = {
  post: PropTypes.any
}

export default Post
