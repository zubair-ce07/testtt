import axios from 'axios'

export const getPaginationProducts = (page) => {
    return (dispatch, getState) => {
        let url = 'http://127.0.0.1:8000/api/products/?page='
        url = url + page + '&Out of Stock=false'
        axios.get(url)
            .then(res => {
                dispatch({ type: 'UPDATE_PRODUCTS', products: res.data.results });
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
