import { LOGIN_SUCCESSFUL , LOGIN_FAILED , LOGOUT_SUCCESSFUL , 
    LOGOUT_FAILED , SIGNUP_SUCCESSFUL, SIGNUP_FAILED, 
    USER_VALUE_UPDATE, CUSTOMER_PROFILE_SUCCESSFUL, CUSTOMER_PROFILE_FAILED ,
    SALOON_PROFILE_FAILED,SALOON_PROFILE_SUCCESSFUL,CUSTOMER_UPDATE_PROFILE_SUCCESSFUL,
    CUSTOMER_UPDATE_PROFILE_FAILED,SALOON_UPDATE_PROFILE_SUCCESSFUL,
    SALOON_UPDATE_PROFILE_FAILED} from '../constants/actionsTypeConstants';

const initState = {
    user: {},
    LoginFailed: false,
    signup_failed:false,
    update_status:false,
};
const userReducer = (state = initState, action) => {
    let response_data;
    switch (action.type) {
    case LOGIN_SUCCESSFUL:
        return {
            ...state,
            LoginFailed: false
        };
    case LOGIN_FAILED:
        return {
            ...state,
            LoginFailed: true
        };
    case LOGOUT_SUCCESSFUL:
        return {
            ...state,
        };
    case LOGOUT_FAILED:
        return {
            ...state,
        };
    case SIGNUP_SUCCESSFUL:
        return {
            ...state,
            signup_failed: false
        };
    case SIGNUP_FAILED:
        return {
            ...state,
            signup_failed: true
        };
    case CUSTOMER_PROFILE_SUCCESSFUL:
        response_data = {
            'phone_no': action.payload.phone_no
        };
        response_data = Object.assign(response_data, action.payload.user);
        return {
            ...state,
            user: response_data,
            update_status: true
        };
    case CUSTOMER_PROFILE_FAILED:
        return {
            ...state,
            update_status: false
        };
    case CUSTOMER_UPDATE_PROFILE_SUCCESSFUL:
        return {
            ...state,
            update_status: true
        };
    case CUSTOMER_UPDATE_PROFILE_FAILED:
        return {
            ...state,
            update_status: false
        };
    case SALOON_UPDATE_PROFILE_SUCCESSFUL:
        return {
            ...state,
            update_status: true
        };
    case SALOON_UPDATE_PROFILE_FAILED:
        return {
            ...state,
            update_status: false
        };
    case SALOON_PROFILE_SUCCESSFUL:
        response_data = {
            'phone_no': action.payload.phone_no,
            'address': action.payload.address,
            'shop_name': action.payload.shop_name
        };
        response_data = Object.assign(response_data, action.payload.user);
        return {
            ...state,
            user: response_data,
            update_status: true
        };
    case SALOON_PROFILE_FAILED:
        return {
            ...state,
            update_status: false
        };
    case USER_VALUE_UPDATE:{
        let user_data = { ...state.user };
        user_data[action.payload.key] = action.payload.value;
        return {
            ...state,
            user: user_data
        };
    }
    default:
        return state;
    }
};
export default userReducer;