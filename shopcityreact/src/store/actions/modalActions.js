import axios from 'axios';
import { CHANGE_MODAL_STATE, UPDATE_OPTIONS } from './actions'


export const changeModalState = () => {
    return (dispatch, getState) => {
        dispatch({ type: CHANGE_MODAL_STATE });
    };
};


export const setOptions = () => {
    return (dispatch, getState) => {
        let url = 'http://172.16.14.58:8000/api/options/';
        axios.get(url)
            .then(res => {
                dispatch({ type: UPDATE_OPTIONS, options: res.data });
            });
    };
};
