const defaultState = {
	friends: [],
};
export default function friendReducer(state = defaultState, action) { 
	switch(action.type){
		case("LIST_FRIENDS"):
			return Object.assign({}, state, { 
              friends: action.friends,
            });
        case("UPDATE_FRIENDS"):
        	return Object.assign({}, state, {
        		friends: [
                  action.friend,
        			...state.friends,
	          		
        		]
      		})
        default:
          return state;
	}
}