const initState = {
    saloons: [
        { id: '1', title: 'hello', body: 'asjdasd' },
        { id: '2', title: 'hello2', body: 'asjdasdaasdasasd' },
        { id: '3 ', title: 'hello3', body: 'asjaa232323dasd' }
    ],
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