const initState = {
    user: {},
    LoginFailed: false,
    signup_failed:false,
    update_status:false,
};
const userReducer = (state = initState, action) => {
    let response_data;
    switch (action.type) {
    case 'LOGIN_SUCESSFUL':
        return {
            ...state,
            LoginFailed: false
        };
    case 'LOGIN_FAILED':
        return {
            ...state,
            LoginFailed: true
        };
    case 'LOGOUT_SUCESSFUL':
        return {
            ...state,
        };
    case 'LOGOUT_FAILED':
        return {
            ...state,
        };
    case 'SIGNUP_SUCESSFUL':
        return {
            ...state,
            signup_failed: false
        };
    case 'SIGNUP_FAILED':
        return {
            ...state,
            signup_failed: true
        };
    case 'CUSTOMER_PROFILE_SUCESSFUL':
        response_data = {
            'phone_no': action.payload.phone_no
        };
        response_data = Object.assign(response_data, action.payload.user);
        return {
            ...state,
            user: response_data,
            update_status: true
        };
    case 'CUSTOMER_PROFILE_FAILED':
        return {
            ...state,
            update_status: false
        };
    case 'SALOON_PROFILE_SUCESSFUL':
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
    case 'SALOON_PROFILE_FAILED':
        return {
            ...state,
            update_status: false
        };
    case 'USER_VALUE_UPDATE':{
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