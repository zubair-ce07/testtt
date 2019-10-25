import axios from 'axios'


export const getPaginationProducts = (page, filters) => {
    return (dispatch, getState) => {
        console.log("PAGE AND FILTERS", page, filters)
        let url = "http://127.0.0.1:8000/api/products/?"
        var queryParams = ''
        queryParams = queryParams + 'page=' + page + '&'
        if (filters.brand != ''){
            queryParams = queryParams + ('Brand=' + filters.brand + '&')
        }
        if (filters.size != ''){
            queryParams = queryParams + ('Size=' + filters.size + '&')
        }
        if (filters.colour != ''){
            queryParams = queryParams + ('Colour=' + filters.colour + '&')
        }
        if (filters.category != ''){
            queryParams = queryParams + ('Category=' + filters.category + '&')
        }
        if (filters.name != ''){
            queryParams = queryParams + ('Name=' + filters.name + '&')
        }
        if (filters.minimum != ''){
            queryParams = queryParams + ('Minimum Price=' + filters.minimum + '&')
        }
        if (filters.maximum != ''){
            queryParams = queryParams + ('Maximum Price=' + filters.maximum + '&')
        }
        queryParams = queryParams + 'Out of Stock=' + filters.outOfStock
        url = url + queryParams
        console.log(url)
        axios.get(url)
            .then(res => {
                dispatch({ type: 'GET_PRODUCTS_SUCCESS', payload: { products: res.data.results, filters: filters } });
            }).catch(err => {
                dispatch({ type: 'GET_PRODUCTS_ERROR', error:err });
            })
    };
};


export const nextPage = () => {
    return (dispatch, getState) => {
        dispatch({ type: 'NEXT_PAGE' });
    };
};


export const previousPage = () => {
    return (dispatch, getState) => {
        dispatch({ type: 'PREVIOUS_PAGE' });
    };
};


export const resetPage = () => {
    return (dispatch, getState) => {
        dispatch({ type: 'RESET_PAGE' });
    };
};


export const resetAll = () => {
    return (dispatch, getState) => {
        dispatch({ type: 'RESET_ALL' });
    };
};
