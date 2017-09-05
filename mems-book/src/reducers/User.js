import { SIGNUP_ACTION, GET_USER_PROFILE, UPDATE_PROFILE} from '../constants';


export const signup = function (state=null, action) {
    if (action.type === SIGNUP_ACTION+'_FULFILLED'){
        localStorage.setItem('token', action.payload.data.token);
        localStorage.setItem('user', JSON.stringify(action.payload.data));
        return action.payload.data;
    }else if (action.type === GET_USER_PROFILE+'_FULFILLED') {
        return action.payload.data;
    }else if (action.type === UPDATE_PROFILE+'_FULFILLED') {
        localStorage.setItem('user', JSON.stringify(action.payload.data));
        return action.payload.data;
    }
    return state;
}
