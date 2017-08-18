import { PROFILE_USER } from '../actions';

export default function(state = {}, action) {
    switch(action.type) {
        case PROFILE_USER:
            console.log("User Profile", action.payload.data);
            return action.payload.data;
        default:
            return state;
    }
}