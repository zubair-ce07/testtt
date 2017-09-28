import React from 'react';
import Comment from './Comment'
import AddComment from './AddComment'
import '../StyleSheets/PostList.css'


const CommentList = ({comments, postId}) => {
		let hide_n_show_comments
		if(comments.length > 0)
		{
			hide_n_show_comments = <div style={{marginTop: "2%"}}>
									{
										comments.map( comment => {
											return(
											<div className="commentwell" key={comment.id}> 
												<Comment comment={comment.comment} username={comment.user} />
											</div>
											);
										})
									}
									</div>
		}
		else{
			hide_n_show_comments = <div>No comments found</div>
		}

		return (
			<div>
				{hide_n_show_comments}<br/>
				<AddComment postId={postId}/>
			</div>
		);
}

export default CommentList;