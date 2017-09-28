export const login = (username, token, id) => {
    return {
        type: 'LOGIN',
        username,
        token,
        id
    };
};
 
export const logout = () => {
    return {
        type: 'LOGOUT'
    };
};
 
export const signup = (username, password) => {
    return (dispatch) => {
    };
};