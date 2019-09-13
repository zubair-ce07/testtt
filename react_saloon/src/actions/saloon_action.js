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
        return axios.get('http://127.0.0.1:8000/shop/api/saloons/').then((response) => {
            dispatch({ type: 'FETCH_SALOON_SUCESSFUL', payload: response.data });
        }).catch((err) => {
            dispatch({ type: 'FETCH_SALOON_FAILED' });
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

    // dispatch({ type: 'FETCH_POST', payload: 'asdasdas' });

}

// export const detailPost = (id) => {

//     return dispatch => {
//         axios.get('https://jsonplaceholder.typicode.com/posts/' + id).then((response) => {
//             dispatch({ type: 'DETAIL_POST', payload: response.data });
//         })
//     }

// }