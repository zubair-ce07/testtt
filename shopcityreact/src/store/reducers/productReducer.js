const initState = {
    products: null,
    currentPage: 1
};

const productReducer = (state=initState, action) => {
    if (action.type === 'UPDATE_PRODUCTS') {
        return {
            ...state,
            products: action.products
        }
    }
    if (action.type === 'NEXT_PAGE') {
        return {
            ...state,
            currentPage: state.currentPage + 1
        }
    }
    if (action.type === 'PREVIOUS_PAGE') {
        return {
            ...state,
            currentPage: state.currentPage - 1
        }
    }
    return state;
};

export default productReducer;
