import axios from 'axios';

import {
    LOADING_MORE,
    LOADED_MORE
} from './action_types'


export function fetchMore(url) {
    return dispatch => {
        dispatch({type: LOADING_MORE, url});
        const request = axios.get(url);

        dispatch({
            type: LOADED_MORE,
            payload: request
        });
    };
}
