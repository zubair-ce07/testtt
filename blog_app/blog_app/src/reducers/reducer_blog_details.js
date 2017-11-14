import { FETCH_BLOG } from '../config'

const INITIAL_STATE = { all: [], post: null };

export default function(state=INITIAL_STATE, action)
{
    switch (action.type){
        case FETCH_BLOG:
            return { all: state.all, post: action.payload.data };
        default:
            return state;
    }
}