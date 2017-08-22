import { INTERESTS_USER, UPDATE_INTERESTS } from '../actions';

export default function(state = [], action) {
    switch(action.type) {
        case INTERESTS_USER:
            return action.payload.data;
        case UPDATE_INTERESTS:
            return action.payload.data;
        default:
            return state;
    }
}