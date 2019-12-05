import React, { useState } from 'react'
import PropTypes from 'prop-types'

import Comment from 'components/Home/Comment/CommentComponent'
import CreateUpdateComment from 'components/Home/Comment/CreateUpdateComponent'
export const CommentsPanel = ({ post, comments }) => {
  const [enableComment, changeEnableComment] = useState(false)

  return (
    <>
      <div className="card-footer">
        <span className="card-link" onClick={() => { changeEnableComment(true) }}><i className="fa fa-comment"></i> Comment</span>
      </div>

      <div className="row bootstrap snippets">
        <div className="col-md-12 col-md-offset-2 col-sm-12">
          <div className="comment-wrapper">
            <div className="panel panel-info">
              {/* <div className="panel-heading">
                    Comment panel
              </div> */}
              <div className="panel-body">
                { enableComment && <>
                  <CreateUpdateComment post={post}/>
                </>
                }

                <div className="clearfix"></div>
                <hr/>
                <ul className="media-list">
                  {comments.length ? comments.map((comment) => <Comment key={comment.id} post={post} comment={comment}></Comment>) : <></>}
                </ul>
              </div>
            </div>
          </div>

        </div>
      </div>
    </>
  )
}

CommentsPanel.propTypes = {
  comments: PropTypes.any,
  post: PropTypes.any
}

export default CommentsPanel
