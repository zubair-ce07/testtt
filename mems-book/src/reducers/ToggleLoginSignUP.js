import {DISPLAY_LOGIN_TAB, DISPLAY_SIGUP_TAB} from "../constants";

export const ToggleLoginSignUp = (state = 'login', action) => {
    if (action.type === DISPLAY_SIGUP_TAB || action.type === DISPLAY_LOGIN_TAB) {
        return action.payload;
    };
    return state;
};
