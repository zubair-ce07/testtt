export const listUsers = (users) => {
	return {
		type: "LIST_USERS",
		users,
	};
}

export const friendAdded = (friend) => {
	return{
		type: "FRIEND_ADDED",
		friend
	}
}
