const defaultState = {
    isLoggedIn: false,
    username: '',
    token: '',
    id: ''
};
 
export default function authReducer(state = defaultState, action) {
    switch (action.type) {
        case 'LOGIN':
            return Object.assign({}, state, { 
                isLoggedIn: true,
                username: action.username,
                token: action.token,
                id: action.id
            });
        case 'LOGOUT':
            return Object.assign({}, state, { 
                isLoggedIn: false,
                username: '',
                token: '',
                id: ''
            });
        default:
            return state;
    }
}