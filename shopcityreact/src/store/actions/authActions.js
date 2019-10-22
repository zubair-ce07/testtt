import axios from 'axios';

export const authorizeUser = (user) => {
    return (dispatch, getState) => {
        let url = 'http://127.0.0.1:8000/api/token/'
        let data = {username: user.username, password: user.password}
        axios.post(url, data)
            .then((res) => {
                switch (res.status) {
                    case 200:
                        user = {
                            ...user,
                            isAuthenticated: true,
                            authorizationToken: res.data.access
                        }
                        dispatch({ type: 'CHANGE_USER', user: user })
                    default:
                        console.log(res)
                }
            }).catch((err) => {
                console.log(err)
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
                switch (res.status) {
                    case 201:
                        user = {
                            ...user,
                            isAuthenticated: true,
                            authorizationToken: res.data.access
                        }
                        dispatch({ type: 'CHANGE_USER', user: user })
                    default:
                        console.log(res)
                }
            }).catch((err) => {
                console.log(err)
            })
    };
};
