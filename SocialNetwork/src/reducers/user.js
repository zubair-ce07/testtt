import { LIST_USERS, FRIEND_ADDED} from '../actions/actions'

const defaultState = {
    users: []
};
export default function userReducer(state = defaultState, action) { 
	switch(action.type){
		case LIST_USERS:
			return{ 
        users: action.users,
      });
    case FRIEND_ADDED:
      return { users: state.users.map(user => 
          (user.id === action.friend.id)
          ? {...user, is_friend: true}
          : user
      )};
    default:
      return state;
	}
}