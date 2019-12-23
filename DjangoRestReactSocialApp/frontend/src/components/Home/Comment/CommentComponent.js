import React, { useState } from 'react'
import { useDispatch } from 'react-redux'
import PropTypes from 'prop-types'

import { deleteComment } from 'store/modules/comment/comment.action'

import { confirmBox, toast } from 'helpers/common'
import CreateComment from './CreateUpdateComponent'
import CommentView from './ViewComponent'

export const Comment = ({ comment, post }) => {
  const dispatch = useDispatch()

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
        <CommentView actionHandler={actionHandler} comment={comment}></CommentView>
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
