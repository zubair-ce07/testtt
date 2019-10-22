const initState = {
    user: {
        username: '',
        password: '',
        isAuthenticated: false,
        authorizationToken: ''
    }
};

const authReducer = (state=initState, action) => {
    switch (action.type) {
        case 'CHANGE_USER':
            return {
                ...state,
                user: action.user
            };
        case 'LOGOUT_USER':
                return {
                    ...state,
                    user: {
                        username: '',
                        password: '',
                        isAuthenticated: false,
                        authorizationToken: ''
                    }
                };
        default:
            return state;
    }

};

export default authReducer;
