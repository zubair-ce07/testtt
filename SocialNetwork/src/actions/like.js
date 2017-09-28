export const listLike = (likes) => {
	return {
		type: "LIST_LIKES",
		likes,
	};
}

export const addLike = (like) => {
	return {
		type: "ADD_LIKE",
		like
	}
}