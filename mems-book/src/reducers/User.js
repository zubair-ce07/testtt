import {GET_USER_PROFILE, SIGNUP_ACTION, SUCCESS, UPDATE_PROFILE} from "../constants";

export const signup = function (state = null, action) {
    if (action.type === SIGNUP_ACTION + SUCCESS) {
        localStorage.setItem('token', action.payload.data.token);
        localStorage.setItem('user', JSON.stringify(action.payload.data));
        return action.payload.data;
    } else if (action.type === GET_USER_PROFILE + SUCCESS) {
        return action.payload.data;
    } else if (action.type === UPDATE_PROFILE + SUCCESS) {
        localStorage.setItem('user', JSON.stringify(action.payload.data));
        return action.payload.data;
    };
    return state;
};
