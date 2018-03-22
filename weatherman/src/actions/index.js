
import * as actionType from './actionTypes';


export const loadWeatherRequest= ()=> ({
    type: actionType.LOAD_WEATHER_REQUEST
})
export const loadWeatherSuccess= (weather)=> ({
    type: actionType.LOAD_WEATHER_SUCCESS, weather
})

export const loadWeatherFailed= (error)=> ({
    type: actionType.LOAD_WEATHER_FAILED, error
})