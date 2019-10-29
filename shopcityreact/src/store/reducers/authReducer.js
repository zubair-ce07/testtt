import { LOGIN_PENDING, LOGIN_ERROR, LOGIN_SUCCESS,
    LOGOUT_USER, REGISTER_ERROR, REGISTER_SUCCESS,
    REGISTER_PENDING, UPDATE_SUCCESS, UPDATE_ERROR,
    UPDATE_CART, ADD_TO_CART, CHECKOUT } from '../actions/actions';


const initState = {
    user: {
        id: null,
        username: '',
        password: '',
        firstName: '',
        lastName: '',
        email: '',
        cart: null,
        address: '',
        state: '',
        city: '',
        zipCode: '',
        contact: '',
        isAuthenticated: false,
        authorizationToken: '',
        isSuperUser: false
    },
    loginPending: true,
    loginError: null,
    registerPending: true,
    registerError: null,
    updateError: null,
    cart: [
        {
            status: 'Current',
            cart_items: []
        }
    ]
};


const authReducer = (state=initState, action) => {
    switch (action.type) {
        case LOGIN_PENDING:
                return {
                    ...state,
                    loginPending: true
                };
        case LOGIN_ERROR:
                return {
                    ...state,
                    loginError: action.payload.error
                };
        case LOGIN_SUCCESS:
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
        case LOGOUT_USER:
                return {
                    user: {
                        id: null,
                        username: '',
                        password: '',
                        firstName: '',
                        lastName: '',
                        email: '',
                        cart: null,
                        address: '',
                        state: '',
                        city: '',
                        zipCode: '',
                        contact: '',
                        isAuthenticated: false,
                        authorizationToken: '',
                        isSuperUser: false
                    },
                    loginPending: true,
                    loginError: null,
                    registerPending: true,
                    registerError: null,
                    updateError: null,
                    cart: [
                        {
                            status: 'Current',
                            cart_items: []
                        }
                    ]
                };
        case REGISTER_PENDING:
                return {
                    ...state,
                    registerPending: true
                };
        case REGISTER_ERROR:
                return {
                    ...state,
                    registerError: action.error
                };
        case REGISTER_SUCCESS:
            return {
                ...state,
                registerError: null,
                registerPending: false
            };
        case UPDATE_SUCCESS:
                return {
                    ...state,
                    user: action.payload.user,
                    updateError: null
                };
        case UPDATE_ERROR:
                return {
                    ...state,
                    updateError: action.payload.error
                };
        case ADD_TO_CART:
            return {
                ...state,
                cart: [
                    {
                        ...state.cart[0],
                        cart_items: [...state.cart[0].cart_items, action.payload.cartItem]
                    }
                ]
            }
        case UPDATE_CART:
            return {
                ...state,
                cart: action.payload.cart
            }
        case CHECKOUT:
                return {
                    ...state,
                    cart: [
                        {
                            status: 'Current',
                            cart_items: []
                        }
                    ]
                }
        default:
            return state;
    };

};

export default authReducer;
