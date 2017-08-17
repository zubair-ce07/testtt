import { LOGIN_USER } from '../actions';

export default function(state = {}, action) {
    switch(action.type) {
        case LOGIN_USER:
            console.log("User Token: ",action.payload)
            return action.payload.data
        default:
            return state;
    }
}