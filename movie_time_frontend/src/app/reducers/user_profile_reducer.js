import {FETCH_USER, SEND_FOLLOW_REQUEST, UPDATE_USER} from '../actions/action_types';


export default function (state = null, action) {
    switch (action.type) {
        case FETCH_USER:
        case SEND_FOLLOW_REQUEST:
        case UPDATE_USER:
            return action.payload.data;
        default:
            return state;
    }
}
