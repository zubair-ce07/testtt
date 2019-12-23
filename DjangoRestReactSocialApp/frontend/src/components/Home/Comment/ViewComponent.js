import React from 'react'
import { useSelector } from 'react-redux'
import PropTypes from 'prop-types'
import ReactTimeAgo from 'react-time-ago'
import { resolveImageUrl } from 'helpers/common'

import ActionComponent from 'components/Common/ActionComponent'

export const CommentView = ({ comment, actionHandler }) => {
  const user = useSelector(state => state.user.user)
  return (
    <>
      <span className="pull-left">
        <img src={resolveImageUrl(comment.author.image)} alt="" className="img-circle"/>
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
  )
}

CommentView.propTypes = {
  actionHandler: PropTypes.any,
  comment: PropTypes.any,
  user: PropTypes.any
}

export default CommentView
