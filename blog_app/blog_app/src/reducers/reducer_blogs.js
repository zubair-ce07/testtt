import { FETCH_BLOG_POSTS } from '../config'

const INITIAL_STATE = { all: [], post: null };

export default function(state=INITIAL_STATE, action)
{
    switch (action.type){
        case FETCH_BLOG_POSTS:
            return { all: action.payload.data, post: state.post };
        default:
            return state;
    }
}