import React from 'react';
import '../StyleSheets/PostList.css'


const Comment = ({comment , username}) => {
	return (
			<div className="commentwell">
				<p>{comment}</p>
				<p>comment by {username}</p>
			</div>
		);
}

export default Comment;