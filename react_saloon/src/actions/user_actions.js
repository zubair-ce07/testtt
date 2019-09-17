import axios from 'axios'
import ls from 'local-storage'

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

export const user_value_update = (key, value) => {
    return dispatch => {
        dispatch({ type: 'USER_VALUE_UPDATE', payload: { key, value } });
    }

}