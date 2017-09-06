import { ALL_CATEGORIES } from '../actions';


export default function(state = [], action) {
    switch(action.type) {
        case ALL_CATEGORIES:
            return action.payload.data;
        default:
            return state;
    }
}