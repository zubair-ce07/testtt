import { INTERESTS_USER } from '../actions';

export default function(state = [], action) {
    switch(action.type) {
        case INTERESTS_USER:
            console.log("User Interest", action.payload.data);
            return action.payload.data;
        default:
            return state;
    }
}