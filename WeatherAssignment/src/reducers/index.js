import { combineReducers } from 'redux';

import WeatherResultList from './reducer_weather_list';

const rootReducer = combineReducers({
    weather: WeatherResultList
});

export default rootReducer;
