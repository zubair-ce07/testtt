import { PROFILE_USER, UPDATE_USER_PROFILE } from '../actions';


export default function(state = {}, action) {
    switch(action.type) {
        case PROFILE_USER:
            return action.payload.data;
        case UPDATE_USER_PROFILE:
            return action.payload.data;
        default:
            return state;
    }
}