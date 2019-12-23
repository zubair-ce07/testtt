import React, { useState } from 'react'
import PropTypes from 'prop-types'

import Comment from 'components/Home/Comment/CommentComponent'
import CreateUpdateComment from 'components/Home/Comment/CreateUpdateComponent'

import { Loader } from 'components/Common/ContentLoader'

export const CommentsPanel = ({ post, comments }) => {
  const [enableComment, changeEnableComment] = useState(false)

  return (
    <>
      <div className="card-footer">
        <span className="card-link" onClick={() => { changeEnableComment(!enableComment) }}><i className="fa fa-comment"></i> Comment</span>
      </div>

      <div className="row bootstrap snippets">
        <div className="col-md-12 col-md-offset-2 col-sm-12">
          <div className="comment-wrapper">
            <div className="panel panel-info">
              <div className="panel-body">
                { enableComment && <>
                  <CreateUpdateComment changeEnableComment={changeEnableComment} post={post}/>
                </>
                }

                <div className="clearfix"></div>
                <hr/>
                <Loader type="BlockUi" loadingRef="post.commentLoading">
                  <ul className="media-list">
                    {comments.length ? comments.map((comment) => <Comment key={comment.id} post={post} comment={comment}></Comment>) : <></>}
                  </ul>
                </Loader>
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
