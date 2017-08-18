import { LOGIN_USER } from '../actions';

export default function(state = "", action) {
    switch(action.type) {
        case LOGIN_USER:
            return action.payload.data.token;
        default:
            return state;
    }
}