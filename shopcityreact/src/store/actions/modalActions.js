import axios from 'axios';

export const changeModalState = () => {
    return (dispatch, getState) => {
        dispatch({ type: 'CHANGE_MODAL_STATE' });
    };
};


export const setOptions = () => {
    return (dispatch, getState) => {
        let url = 'http://127.0.0.1:8000/api/options/'
        axios.get(url)
            .then(res => {
                dispatch({ type: 'UPDATE_OPTIONS', options: res.data });
                console.log(res.data)
            })
    };
};
