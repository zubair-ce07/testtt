import {SEARCH_ACTION, API_BASE_URL, APP_ID} from '../constants';
import axios from 'axios';

export const searchWeather = function (dispatch, city) {

    const response = axios.get(API_BASE_URL,{
        params:{
            q: city,
            appid: APP_ID
        }
    });

    response.then(data => { dispatch(search(data))})

    return ({
            type: 'avain',
            payload: response
    });
};

const search = function(data){
    return {
        type:SEARCH_ACTION,
        payload:data
    }
}

