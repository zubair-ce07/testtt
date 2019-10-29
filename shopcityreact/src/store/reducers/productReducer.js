import { GET_PRODUCTS_SUCCESS, GET_PRODUCTS_ERROR, GET_PRODUCTS_PENDING,
    PRODUCT_DETAIL_ERROR, PRODUCT_DETAIL_SUCCESS, UPDATE_PRODUCT,
    NEXT_PAGE, PREVIOUS_PAGE, RESET_PAGE, RESET_ALL } from '../actions/actions';


const initState = {
    products: null,
    product: null,
    productDetailError: null,
    currentPage: 1,
    pending: true,
    error: null,
    filters: {
        brand: '',
        size: '',
        colour: '',
        category: '',
        minimum: '',
        maximum: '',
        name: '',
        outOfStock: false
    }
};

const productReducer = (state=initState, action) => {
    switch (action.type) {
        case GET_PRODUCTS_PENDING:
            return {
                ...state,
                pending: true
            };
        case GET_PRODUCTS_ERROR:
            return {
                ...state,
                pending: false,
                error: action.error
            };
        case GET_PRODUCTS_SUCCESS:
            return {
                ...state,
                pending: false,
                products: action.payload.products,
                filters: action.payload.filters,
                error: null
            };
        case PRODUCT_DETAIL_SUCCESS:
            return {
                ...state,
                product: action.payload.product,
                productDetailError: null
            };
        case PRODUCT_DETAIL_ERROR:
            return {
                ...state,
                productDetailError: action.payload.error
            };
        case UPDATE_PRODUCT:
                return {
                    ...state,
                    product: action.payload.product,
                    productDetailError: null
                };
        case NEXT_PAGE:
            return {
                ...state,
                currentPage: state.currentPage + 1
            };
        case PREVIOUS_PAGE:
            return {
                ...state,
                currentPage: state.currentPage - 1
            };
        case RESET_PAGE:
            return {
                ...state,
                currentPage: 1
            };
        case RESET_ALL:
                return {
                    ...state,
                    products: null,
                    currentPage: 1,
                    pending: true,
                    error: null,
                    filters: {
                        brand: '',
                        size: '',
                        colour: '',
                        category: '',
                        minimum: '',
                        maximum: '',
                        name: '',
                        outOfStock: false
                    }
                };
        };
    return state;
};

export default productReducer;
