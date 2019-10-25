import axios from 'axios';

export const authorizeUser = (user) => {
    return (dispatch, getState) => {
        let url = 'http://127.0.0.1:8000/api/token/'
        let data = {username: user.username, password: user.password}
        axios.post(url, data)
            .then((res) => {
                console.log(res)
                switch (res.status) {
                    case 200:
                        let url = 'http://127.0.0.1:8000/api/users/' + user.username + '/'
                        axios.get(url)
                            .then((response) => {
                                console.log(response)
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
                                        }
                                        let payload = { user: user }
                                        dispatch({ type: 'LOGIN_SUCCESS', payload: payload })
                                }
                            })
                    default:
                        console.log(res)
                }
            }).catch((err) => {
                console.log(err.response)
                dispatch({ type: 'LOGIN_ERROR', payload: {error: err} })
            })
    };
};

export const unauthorizeUser = (user) => {
    return (dispatch, getState) => {
        dispatch({ type: 'LOGOUT_USER'})
    };
};

export const registerUser = (user) => {
    return (dispatch, getState) => {
        let url = 'http://127.0.0.1:8000/api/users/'
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
        }
        console.log(userData)
        axios.post(url, userData)
            .then((res) => {
                console.log(res)
                switch (res.status) {
                    case 201:
                        dispatch({ type: 'REGISTER_SUCCESS'})
                    default:
                        console.log(res)
                }
            }).catch((err) => {
                console.log(err.response)
                dispatch({ type: 'REGISTER_ERROR', error: err })
            })
    };
};

export const updateUser = (user) => {
    return (dispatch, getState) => {
        const previousState = getState()
        let url = 'http://127.0.0.1:8000/api/users/' + previousState.auth.user.username + '/'
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
        }
        axios.patch(url, userData)
            .then((res) => {
                console.log(res)
                switch (res.status) {
                    case 200:
                        console.log(user)
                        dispatch({ type: 'UPDATE_SUCCESS', payload: {user: user}})
                    default:
                        console.log(res)
                }
            }).catch((err) => {
                console.log(err.response)
                dispatch({ type: 'UPDATE_ERROR', payload: {error: err} })
            })
    };
};
