const initState = {
    saloons: [],
    LoginFailed: false
}
const rootReducers = (state = initState, action) => {
    switch (action.type) {
        case 'FETCH_SALOON_SUCESSFUL':
            return {
                ...state,
                saloons: action.payload,
                successStatus: true
            }

        case 'FETCH_SALOON_FAILED':
            return {
                ...state,
                successStatus: false
            }
        case 'LOGIN_SUCESSFUL':
            return {
                ...state,
                LoginFailed: false
            }
        case 'LOGIN_FAILED':
            return {
                ...state,
                LoginFailed: true
            }
        case 'LOGOUT_SUCESSFUL':
            return {
                ...state,
            }
        case 'LOGOUT_FAILED':
            return {
                ...state,
            }
        case 'SIGNUP_SUCESSFUL':
            return {
                ...state,
                signup_failed: false
            }
        case 'SIGNUP_FAILED':
            return {
                ...state,
                signup_failed: true
            }
        case 'CUSTOMER_PROFILE_SUCESSFUL':
            return {
                ...state,
                user: action.payload
            }
        case 'CUSTOMER_PROFILE_FAILED':
            return {
                ...state
            }
        case 'SALOON_PROFILE_SUCESSFUL':
            return {
                ...state,
                user: action.payload
            }
        case 'SALOON_PROFILE_FAILED':
            return {
                ...state
            }

        default:
            return state;
    }
    // if (action.type === 'DELETE_POST') {
    //     let newPosts = state.posts.filter((post) => action.id !== post.id)
    //     return {
    //         ...state,
    //         posts: newPosts,
    //         successStatus: true
    //     }
    // }
    // if (action.type === 'DELETE_POST_FAILED') {
    //     return {
    //         ...state,
    //         successStatus: false
    //     }
    // }
    // if (action.type === 'FETCH_POST') {
    //     return {
    //         ...state,
    //         posts: action.payload
    //     }
    // }
    // return state;
}
export default rootReducers