export const changeModalState = () => {
    return (dispatch, getState) => {
        dispatch({ type: 'CHANGE_MODAL_STATE' });
    };
};
