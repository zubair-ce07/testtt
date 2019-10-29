import axios from 'axios';
import { LOGIN_SUCCESS, LOGIN_ERROR, UPDATE_CART,
    LOGOUT_USER, REGISTER_SUCCESS, REGISTER_ERROR,
    UPDATE_SUCCESS, UPDATE_ERROR, ADD_TO_CART, CHECKOUT } from './actions'


export const authorizeUser = (user) => {
    return (dispatch, getState) => {
        let url = 'http://172.16.14.58:8000/api/token/';
        let data = {username: user.username, password: user.password};

        axios.post(url, data)
            .then((res) => {
                switch (res.status) {
                    case 200:
                        let url = 'http://172.16.14.58:8000/api/users/' + user.username + '/';
                        axios.get(url)
                            .then((response) => {
                                switch (response.status) {
                                    case 200:
                                        user = {
                                            ...user,
                                            id: response.data.id,
                                            firstName: response.data.first_name,
                                            lastName: response.data.last_name,
                                            email: response.data.email,
                                            cart: response.data.cart,
                                            address: response.data.profile.address,
                                            state: response.data.profile.state,
                                            city: response.data.profile.city,
                                            zipCode: response.data.profile.zip_code,
                                            contact: response.data.profile.contact,
                                            isAuthenticated: true,
                                            authorizationToken: res.data.access,
                                            isSuperUser: response.data.is_superuser
                                        };
                                        let payload = { user: user };
                                        dispatch({ type: LOGIN_SUCCESS, payload: payload });
                                };
                            });
                };
            }).catch((err) => {
                dispatch({ type: LOGIN_ERROR, payload: {error: err} })
            });
    };
};


export const updateCart = (user) => {
    console.log('USER:', user)
    return (dispatch, getState) => {
        var cart = null;
        for (let c of user.cart) {
            if (c.state == 'Current') {
                cart = [c];
            };
        };
        if (!cart) {
            cart = [
                {
                    status: "Current",
                    cart_items: []
                }
            ];
        };
        dispatch({ type: UPDATE_CART, payload: { cart: cart } });
    };
};


export const unauthorizeUser = () => {
    return (dispatch, getState) => {
        dispatch({ type: LOGOUT_USER});
    };
};


export const registerUser = (user) => {
    return (dispatch, getState) => {
        let url = 'http://172.16.14.58:8000/api/users/';
        let userData = {
            first_name: user.first_name,
            last_name: user.last_name,
            username: user.username,
            email: user.email,
            is_superuser: false,
            password: user.password,
            profile: {
                address: user.address,
                state: user.state,
                city: user.city,
                zip_code: user.zip_code
            }
        };

        axios.post(url, userData)
            .then((res) => {
                switch (res.status) {
                    case 201:
                        dispatch({ type: REGISTER_SUCCESS});
                        break;
                };
            }).catch((err) => {
                dispatch({ type: REGISTER_ERROR, error: err });
            });
    };
};


export const updateUser = (user) => {
    return (dispatch, getState) => {
        const previousState = getState();
        let url = 'http://172.16.14.58:8000/api/users/' + previousState.auth.user.username + '/';
        let userData = {
            first_name: user.firstName,
            last_name: user.lastName,
            username: user.username,
            email: user.email,
            profile: {
                address: user.address,
                state: user.state,
                city: user.city,
                zip_code: user.zipCode
            }
        };

        axios.patch(url, userData)
            .then((res) => {
                switch (res.status) {
                    case 200:
                        dispatch({ type: UPDATE_SUCCESS, payload: { user: user }});
                        break;
                };
            }).catch((err) => {
                dispatch({ type: UPDATE_ERROR, payload: { error: err }});
            });
    };
};


export const addToCart = (cartItemRaw) => {
    return (dispatch, getState) => {
        const cartItem = {
            quantity: cartItemRaw.quantity,
            sku_id: cartItemRaw.skuId,
            product: cartItemRaw.productId
        };
        const previousState = getState();
        let url = 'http://172.16.14.58:8000/api/users/' + previousState.auth.user.username + '/';
        let cartData = {
            cart: [
                {
                    ...previousState.auth.cart[0],
                    cart_items: [
                        ...previousState.auth.cart[0].cart_items,
                        cartItem
                    ]
                }
            ]
        };
        axios.patch(url, cartData)
            .then((res) => {
                switch (res.status) {
                    case 200:
                        dispatch({ type: ADD_TO_CART, payload: {cartItem: cartItem} });
                        break;
                };
            });
    };
};


export const checkout = () => {
    return (dispatch, getState) => {
        const previousState = getState();
        let url = 'http://172.16.14.58:8000/api/users/' + previousState.auth.user.username + '/';
        let cartData = {
            cart: [
                {
                    ...previousState.auth.cart[0],
                    state: 'Processed'
                }
            ]
        };
        axios.patch(url, cartData)
            .then((res) => {
                switch (res.status) {
                    case 200:
                        dispatch({ type: CHECKOUT });
                        break;
                };
            });
    };
};
