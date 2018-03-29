import weatherApi from '../api/weatherApi';
import {loadWeatherSuccess, loadWeatherFailed, loadWeatherRequest} from './index';

export function loadWeather(name) {
    return function(dispatch) {
        dispatch(loadWeatherRequest());
        return weatherApi.getWeatherData(name).then(weather => {

            dispatch(loadWeatherSuccess(weather));

        }).catch(error => {

            dispatch(loadWeatherFailed(error));
        });
    }
}