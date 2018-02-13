import { LIST_FRIENDS, UPDATE_FRIENDS} from '../actions/actions'

const defaultState = {
	friends: [],
};
export default function friendReducer(state = defaultState, action) { 
	switch(action.type){
		case LIST_FRIENDS:
			return{ 
        friends: action.friends,
      });
    case UPDATE_FRIENDS:
    	return{
    		friends: state.friends.concat(action.friend)
  		})
    default:
      return state;
	}
}