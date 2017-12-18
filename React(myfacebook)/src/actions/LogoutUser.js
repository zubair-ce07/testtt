import { browserHistory } from "react-router";


export function LogoutUser(props) {

    localStorage.clear();
    browserHistory.push('/');

    return {
        type: 'USER_LOGOUT',
        payload: null
    };
}