import { LIST_COMMENTS, ADD_COMMENT} from '../actions/actions'

const defaultState = {
	comments: [],

};
export default function commentReducer(state = defaultState, action) { 
	switch(action.type){
		case LIST_COMMENTS:
			return {comments: state.comments.concat(action.comments)}
      	case ADD_COMMENT:
      		return {
            comments: state.comments.map( (commentsById) => {
    					if(Object.keys(commentsById)[0] === Object.keys(action.comment)[0])
    					{	
    						let updated = commentsById
    						updated[Object.keys(commentsById)[0]] = commentsById[Object.keys(commentsById)[0]].concat(Object.values(action.comment))
    						return updated
    					}
    					else{
    						return commentsById
    					}
    				})
      		}
        default:
          return state;
	}
}