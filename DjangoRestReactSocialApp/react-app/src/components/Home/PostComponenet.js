import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import PropTypes from 'prop-types'
import ReactTimeAgo from 'react-time-ago'
import CommentsPanel from './CommentsPanelComponent'

import { deletePost } from 'store/modules/post/post.action'

import { resolveImageUrl, confirmBox, toast } from 'helpers/common'
import ActionComponent from 'components/Common/ActionComponent'

export const Post = ({ post }) => {
  const dispatch = useDispatch()
  const user = useSelector(state => state.user.user)

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
      <div className="card-body">
        <div className="text-muted h7 mb-2"> <i className="fa fa-clock-o"></i>
          <ReactTimeAgo date={new Date(post.updated_at).getTime()} />
        </div>
        <span className="card-link">
          <h5 className="card-title">{post.title}</h5>
        </span>
        <img src={resolveImageUrl(post.image)} alt="Italian Trulli" />
        {post.body}
      </div>

      <CommentsPanel post={post} comments={post.comments}></CommentsPanel>
    </div>

  )
}

Post.propTypes = {
  post: PropTypes.any
}

export default Post
