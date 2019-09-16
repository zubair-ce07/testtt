import axios from 'axios'
import ls from 'local-storage'

// export const deletePost = (id) => {
//     return dispatch => {
//         return axios.delete('https://jsonplaceholder.typicode.com/posts/id').then((response) => {
//             dispatch({ type: 'DELETE_POST', id });
//             return response
//         }).catch(function (error) {
//             dispatch({ type: 'DELETE_POST_FAILED' })
//             return error
//         })
//     }
// }

export const fetchSaloons = () => {

    return dispatch => {
        return axios.get('http://localhost:8000/shop/api/saloons/').then((response) => {
            dispatch({ type: 'FETCH_SALOON_SUCESSFUL', payload: response.data });
        }).catch((err) => {
            dispatch({ type: 'FETCH_SALOON_FAILED' });
        })
    }

}

export const customer_profile = () => {

    return dispatch => {
        const AuthStr = 'Token '.concat(ls.get('token'));
        return axios.get('http://localhost:8000/customer/api/profile/', { headers: { Authorization: AuthStr } }).then((response) => {
            dispatch({ type: 'CUSTOMER_PROFILE_SUCESSFUL', payload: response.data });
        }).catch((err) => {
            dispatch({ type: 'CUSTOMER_PROFILE_FAILED' });
        })
    }

}

export const saloon_profile = () => {

    return dispatch => {
        const AuthStr = 'Token '.concat(ls.get('token'));
        return axios.get('http://localhost:8000/shop/api/profile/', { headers: { Authorization: AuthStr } }).then((response) => {
            dispatch({ type: 'SALOON_PROFILE_SUCESSFUL', payload: response.data });
        }).catch((err) => {
            dispatch({ type: 'SALOON_PROFILE_FAILED' });
        })
    }

}

export const login = (username, password) => {
    return dispatch => {
        return axios.post('http://localhost:8000/api/login/', { username, password }).then((response) => {
            ls.set('username', response.data.user.username)
            ls.set('email', response.data.user.email)
            ls.set('token', response.data.token)
            ls.set('user_type', response.data.user_type)
            dispatch({ type: 'LOGIN_SUCESSFUL', payload: response.data });
            return response
        }).catch((err) => {
            dispatch({ type: 'LOGIN_FAILED' });
            return err
        })
    }
}

export const logout = () => {
    return dispatch => {
        return axios.get('http://localhost:8000/api/logout/').then((response) => {
            ls.clear()
            dispatch({ type: 'LOGOUT_SUCESSFUL' });
            return response
        }).catch((err) => {
            dispatch({ type: 'LOGOUT_FAILED' });
            return err
        })
    }
}

export const signup = (username, email, password1, password2, user_type) => {
    return dispatch => {
        return axios.post('http://localhost:8000/api/register/', { username, email, password1, password2, user_type }).then((response) => {
            dispatch({ type: 'SIGNUP_SUCESSFUL', payload: response.data });
            return response
        }).catch((err) => {
            console.log(err.response)
            dispatch({ type: 'SIGNUP_FAILED' });
            return err
        })
    }
}