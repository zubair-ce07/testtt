// index.js

import * as actionType from './actionTypes';



export const loadWeatherSuccess= (weather)=> ({
    type: actionType.LOAD_WEATHER_SUCCESS, weather
})

export const loadWeatherFailed= (error)=> ({
    type: actionType.LOAD_WEATHER_FAILED, error
})