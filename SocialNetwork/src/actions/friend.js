export const listFriend = (friends) => {
	return {
		type: "LIST_FRIENDS",
		friends,
	};
}

export const updateFriends = (friend) => {
	return{
		type: "UPDATE_FRIENDS",
		friend
	}
}