const defaultState = {
    users: []
};
export default function userReducer(state = defaultState, action) { 
	switch(action.type){
		case("LIST_USERS"):
			return Object.assign({}, state, { 
                users: action.users,
            });
        case("FRIEND_ADDED"):
            let users = state.users.map(user => 
                (user.id === action.friend.id)
                ? {...user, is_friend: true}
                : user
            );
            return {users}
        default:
            return state;
	}
}