import { FETCH_NEWS_TOP } from '../actions';


export default function(state = [], action) {
    switch(action.type) {
        case FETCH_NEWS_TOP:
            return action.payload.data;
        default:
            return state;
    }
}