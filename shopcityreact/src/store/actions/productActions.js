import axios from 'axios';
import { GET_PRODUCTS_SUCCESS, GET_PRODUCTS_ERROR, NEXT_PAGE, PREVIOUS_PAGE,
    RESET_PAGE, RESET_ALL, PRODUCT_DETAIL_SUCCESS, PRODUCT_DETAIL_ERROR, UPDATE_PRODUCT } from './actions';


export const getPaginationProducts = (page, filters) => {
    return (dispatch, getState) => {
        let url = "http://172.16.14.58:8000/api/products/?";
        var queryParams = '';
        queryParams = queryParams + 'page=' + page + '&';

        if (filters.brand != ''){
            queryParams = queryParams + ('Brand=' + filters.brand + '&');
        };
        if (filters.size != ''){
            queryParams = queryParams + ('Size=' + filters.size + '&');
        };
        if (filters.colour != ''){
            queryParams = queryParams + ('Colour=' + filters.colour + '&');
        };
        if (filters.category != ''){
            queryParams = queryParams + ('Category=' + filters.category + '&');
        };
        if (filters.name != ''){
            queryParams = queryParams + ('Name=' + filters.name + '&');
        };
        if (filters.minimum != ''){
            queryParams = queryParams + ('Minimum Price=' + filters.minimum + '&');
        };
        if (filters.maximum != ''){
            queryParams = queryParams + ('Maximum Price=' + filters.maximum + '&');
        };

        queryParams = queryParams + 'Out of Stock=' + filters.outOfStock;
        url = url + queryParams;

        axios.get(url)
            .then(res => {
                dispatch(
                    { type: GET_PRODUCTS_SUCCESS, payload: { products: res.data.results, filters: filters } }
                );
            }).catch(err => {
                dispatch({ type: GET_PRODUCTS_ERROR, error:err });
            });
    };
};


export const nextPage = () => {
    return (dispatch, getState) => {
        dispatch({ type: NEXT_PAGE });
    };
};


export const previousPage = () => {
    return (dispatch, getState) => {
        dispatch({ type: PREVIOUS_PAGE });
    };
};


export const resetPage = () => {
    return (dispatch, getState) => {
        dispatch({ type: RESET_PAGE });
    };
};


export const resetAll = () => {
    return (dispatch, getState) => {
        dispatch({ type: RESET_ALL });
    };
};


export const getProductDetail = (productId) => {
    return (dispatch, getState) => {
        axios.get('http://172.16.14.58:8000/api/products/' + productId + '/')
        .then(res => {
            dispatch({ type: PRODUCT_DETAIL_SUCCESS, payload: {product: res.data} });
        }).catch( err => {
            dispatch({ type: PRODUCT_DETAIL_ERROR, payload: {error: err} });
        });
    };
};


export const setOutOfStock = (productDetails) => {
    return (dispatch, getState) => {
        var url = 'http://172.16.14.58:8000/api/products/' + productDetails.productId + '/';
        var productData = {
            skus: [
                {
                    sku_id: productDetails.skuId,
                    out_of_stock: true
                }
            ]
        };

        axios.patch(url, productData)
        .then(res => {
            if (res.status == 200) {
                dispatch({ type: UPDATE_PRODUCT, payload: {product: res.data} });
            }
        });
    };
};
