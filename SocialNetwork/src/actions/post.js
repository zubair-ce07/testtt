export const listPost = (posts,posts_count,likes_count) => {
	return {
		type: "LIST_POSTS",
		posts,
		posts_count,
		likes_count,
	};
}

export const addPost = (post) => {
	return {
		type: "ADD_POST",
		post
	};
}

export const postLiked = (id) => {
	return {
		type: "POST_LIKED",
		postId: id
	}
}

export const privacyChanged = (id, privacy) =>{
	return {
		type: "PRIVACY_CHANGED",
		postId: id,
		privacy
	}
}