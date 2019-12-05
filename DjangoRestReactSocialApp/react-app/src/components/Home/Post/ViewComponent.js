import React from 'react'
import PropTypes from 'prop-types'
import ReactTimeAgo from 'react-time-ago'

import { resolveImageUrl } from 'helpers/common'

export const PostView = ({ post }) => {
  return (
    <div className="card-body">
      <div className="text-muted h7 mb-2"> <i className="fa fa-clock-o"></i>
        <ReactTimeAgo date={new Date(post.updated_at).getTime()} />
      </div>
      <span className="card-link">
        <h5 className="card-title">{post.title}</h5>
      </span>
      <img src={resolveImageUrl(post.image)} alt="" />
      {post.body}
    </div>
  )
}

PostView.propTypes = {
  post: PropTypes.any
}

export default PostView
