const initState = {
    cart: {
        cartItems: []
    },
};

const cartReducer = (state=initState, action) => {
    switch (action.type) {
        case 'LOGIN_PENDING':
                return {
                    ...state,
                    loginPending: true
                };
        case 'LOGIN_ERROR':
                return {
                    ...state,
                    loginError: action.payload.error
                };
        case 'LOGIN_SUCCESS':
            return {
                ...state,
                user: {
                    ...state.user,
                    ...action.payload.user
                },
                loginError: null,
                loginPending: false,
                registerError: null,
                registerPending: true
            };
        default:
            return state;
    }

};

export default cartReducer;
