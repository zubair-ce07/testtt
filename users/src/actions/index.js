export const selectUser = (user) => {
    return {
        type: 'SELECT_USER',
        payload:user
    };
};

export const addUser = (user) => {
    return {
        type :'ADD_USER',
        payload: user
    }
}
