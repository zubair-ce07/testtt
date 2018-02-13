import { LIST_LIKES, ADD_LIKE} from '../actions/actions'

const defaultState = {
	likes: [],

};
export default function likeReducer(state = defaultState, action) { 
	switch(action.type){
		case LIST_LIKES:
			return {
        likes: state.likes.concat(action.likes)
      }
  	case ADD_LIKE:
  		return {
  			likes: state.likes.map((likeById) => {
					if(Object.keys(likeById)[0] === Object.keys(action.like)[0])
					{	
						let updated = likeById
						updated[Object.keys(likeById)[0]] = likeById[Object.keys(likeById)[0]].concat(Object.values(action.like))
						return updated
					}
					else{
						return likeById
					}
			 })
  		}
    default:
      return state;
	}
}