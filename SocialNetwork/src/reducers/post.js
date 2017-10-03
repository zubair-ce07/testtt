import { LIST_POSTS, ADD_POST, POST_LIKED, PRIVACY_CHANGED} from '../actions/actions'

const defaultState = {
	posts: [],
	posts_count: 0,
	likes_count: 0,
};
export default function postReducer(state = defaultState, action) { 
	switch(action.type){
		case LIST_POSTS:
			return Object.assign({}, state, { 
              posts: action.posts,
              posts_count: action.posts_count,
              likes_count: action.likes_count,
            });
        case ADD_POST:
        	return Object.assign({}, state, {
        		posts: [
                  action.post,
        			...state.posts,
        		]
      		})
        case POST_LIKED:
            return {
              ...state,
              posts: state.posts.map(post => {
                      return (
                        post["id"] === action.postId
                        ? {...post, is_liked: true}
                        : post
                      );
                  })
            }
        case PRIVACY_CHANGED:
            return {
              ...state,
              posts: state.posts.map(post => {
                      return (
                        post["id"] === action.postId
                        ? {...post, privacy: action.privacy}
                        : post
                      );
                  })
            }
        default:
          return state;
	}
}