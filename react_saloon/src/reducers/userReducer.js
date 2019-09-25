import { actionTypes } from '../constants/actionsTypeConstants';

const initState = {
    user: {},
    LoginFailed: false,
    signupFailed:false,
    updateStatus:false,
};
const userReducer = (state = initState, action) => {
    let responseData;
    switch (action.type) {
    case actionTypes.LOGIN_SUCCESSFUL:
        return {
            ...state,
            LoginFailed: false
        };
    case actionTypes.LOGIN_FAILED:
        return {
            ...state,
            LoginFailed: true
        };
    case actionTypes.LOGOUT_SUCCESSFUL:
        return {
            ...state,
        };
    case actionTypes.LOGOUT_FAILED:
        return {
            ...state,
        };
    case actionTypes.SIGNUP_SUCCESSFUL:
        return {
            ...state,
            signupFailed: false
        };
    case actionTypes.SIGNUPFAILED:
        return {
            ...state,
            signupFailed: true
        };
    case actionTypes.CUSTOMER_PROFILE_SUCCESSFUL:
        responseData = {
            'phone_no': action.payload.phone_no
        };
        responseData = Object.assign(responseData, action.payload.user);
        return {
            ...state,
            user: responseData,
            updateStatus: true
        };
    case actionTypes.CUSTOMER_PROFILE_FAILED:
        return {
            ...state,
            updateStatus: false
        };
    case actionTypes.CUSTOMER_UPDATE_PROFILE_SUCCESSFUL:
        return {
            ...state,
            updateStatus: true
        };
    case actionTypes.CUSTOMER_UPDATE_PROFILE_FAILED:
        return {
            ...state,
            updateStatus: false
        };
    case actionTypes.SALOON_UPDATE_PROFILE_SUCCESSFUL:
        return {
            ...state,
            updateStatus: true
        };
    case actionTypes.SALOON_UPDATE_PROFILE_FAILED:
        return {
            ...state,
            updateStatus: false
        };
    case actionTypes.SALOON_PROFILE_SUCCESSFUL:
        responseData = {
            'phone_no': action.payload.phone_no,
            'address': action.payload.address,
            'shop_name': action.payload.shop_name
        };
        responseData = Object.assign(responseData, action.payload.user);
        return {
            ...state,
            user: responseData,
            updateStatus: true
        };
    case actionTypes.SALOON_PROFILE_FAILED:
        return {
            ...state,
            updateStatus: false
        };
    case actionTypes.USER_VALUE_UPDATE:{
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