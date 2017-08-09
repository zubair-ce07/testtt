import { WEATHERMAP_API_KEY, FETCH_WEATHER, WEATHERMAP_ROOT_URL } from '../config'
import axios from 'axios';


export function fetchWeather(city)
{
    const response = axios.get(WEATHERMAP_ROOT_URL,{
        params:{
            q: city,
            units: 'metric',
            appid: WEATHERMAP_API_KEY
        }
    });

    return ({
        type: FETCH_WEATHER,
        payload: response
    })
}