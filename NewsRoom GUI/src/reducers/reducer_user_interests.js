import { INTERESTS_USER, UPDATE_INTERESTS } from '../actions';

export default function(state = [], action) {
    switch(action.type) {
        case INTERESTS_USER:
            console.log("User Interest", action.payload.data);
            return action.payload.data;
        case UPDATE_INTERESTS:
            console.log("Update User Interest", action.payload.data);
            return action.payload.data;
        default:
            return state;
    }
}