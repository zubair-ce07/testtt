import React, { useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import PropTypes from 'prop-types'
import ReactTimeAgo from 'react-time-ago'

import { deleteComment } from 'store/modules/comment/comment.action'

import { confirmBox, toast } from 'helpers/common'
import ActionComponent from 'components/Common/ActionComponent'
import CreateComment from './CreateCommentComponent'

export const Comment = ({ comment, post }) => {
  const dispatch = useDispatch()
  const user = useSelector(state => state.user.user)

  const [mode, modeChange] = useState('view')

  const actionHandler = (type) => {
    if (type === 'delete') {
      confirmBox((result) => {
        dispatch(deleteComment(comment.id)).then((res) => {
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

    <li className="media">
      { mode === 'view' ? <>
        <span className="pull-left">
          <img src="https://bootdey.com/img/Content/user_1.jpg" alt="" className="img-circle"/>
        </span>
        <div className="media-body">
          <span className="text-muted pull-right">
            <small className="text-muted"><ReactTimeAgo date={new Date(comment.updated_at).getTime()}/></small>
            {user.id === comment.author.id && <ActionComponent actionHandler={actionHandler}></ActionComponent>}

          </span>
          <strong className="text-success">@{comment.author.username}</strong>
          <p>
            {comment.comment}
          </p>
        </div>
      </>
        : <CreateComment post={post} modeChange={modeChange} comment={comment} mode="edit"></CreateComment>}
    </li>

  )
}

Comment.propTypes = {
  comment: PropTypes.any,
  post: PropTypes.any
}

export default Comment
