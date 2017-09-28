export const listComment = (comments) => {
	return {
		type: "LIST_COMMENTS",
		comments,
	};
}

export const addComment = (comment) => {
	return {
		type: "ADD_COMMENT",
		comment
	}
}