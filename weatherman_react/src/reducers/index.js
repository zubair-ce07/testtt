import { combineReducers } from 'redux'

import cityReducer from './cityReducer'
import yearReducer from './yearReducer'
import { yearlyWeather, monthlyWeather } from './weatherReducer'

export default combineReducers({
    cities: cityReducer,
    years: yearReducer,
    yearlyWeather: yearlyWeather,
    monthlyWeather: monthlyWeather,
})