import axios from 'axios';

const BASE_URL = 'http://api.openweathermap.org/data/2.5/forecast?appid=198c6e1e72c287674ae7d1888c8f9cff';

export function  getWeather(cityName) {

    const url = `${BASE_URL}&q=${cityName},us`;
    const request = axios.get(url);

    return({
            type: 'GET_WEATHER',
            payload: request
        }
    )

}