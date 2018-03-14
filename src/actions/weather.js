// src/actions/catActions.js

import weatherApi from '../api/weatherApi';
import {loadWeatherSuccess, loadWeatherFailed} from './index';


export function loadWeatherData(name='') {
    return function(dispatch) {
        return weatherApi.getWeatherData(name).then(weather => {
            dispatch(loadWeatherSuccess(weather));
        }).catch(error => {
            dispatch(loadWeatherFailed(error));
        });
    };
}