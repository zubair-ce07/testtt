import {combineReducers} from 'redux';
import weatherData from './weather-data';


const allReducers = combineReducers({
    weatherData
});
export default allReducers;
