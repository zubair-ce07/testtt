import {LOGIN_ACTION, LOGOUT_ACTION, SUCCESS} from "../constants";

export const Token = function (state = null, action) {
    if (action.type === LOGIN_ACTION + SUCCESS) {
        if (action.payload.data.token) {
            localStorage.setItem('token', action.payload.data.token);
            localStorage.setItem('user', JSON.stringify(action.payload.data));
            return action.payload.data.token;
        } else {
            // this means username or passsword is not correct
            return false;
        };
    } else if (action.type === LOGOUT_ACTION + SUCCESS) {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        return null;
    }
    return state;
};
