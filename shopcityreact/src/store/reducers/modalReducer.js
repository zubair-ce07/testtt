const initState = {
    modalOpen: false
};

const modalReducer = (state=initState, action) => {
    if (action.type === 'CHANGE_MODAL_STATE') {
        return {
            ...state,
            modalOpen: !state.modalOpen
        }
    }
    return state;
};

export default modalReducer;
