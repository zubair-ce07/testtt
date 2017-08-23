import { USER_LOGOUT } from "../config"
import { browserHistory } from "react-router";


export function logoutUser(props) {

    localStorage.clear();
    browserHistory.push('/');

    return {
        type: USER_LOGOUT,
        payload: null
    };
}