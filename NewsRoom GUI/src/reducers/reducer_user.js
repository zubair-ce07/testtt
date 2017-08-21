import { PROFILE_USER, UPDATE_USER_PROFILE } from '../actions';

export default function(state = {}, action) {
    switch(action.type) {
        case PROFILE_USER:
            console.log("User Profile", action.payload.data);
            return action.payload.data;
        case UPDATE_USER_PROFILE:
            console.log("User Updated Profile: ", action.payload.data);
            return action.payload.data;
        default:
            return state;
    }
}