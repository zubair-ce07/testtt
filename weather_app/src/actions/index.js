import axios from 'axios'

export const searchByCity = (city_name) => {
    return dispatch => {return getWeatherData(city_name).then(response => dispatch(searchCity(response.data)))};
};

const getWeatherData = (city_name) => {
        return axios.get('http://api.openweathermap.org/data/2.5/forecast?',{
            params:{
                q: city_name,
                appid: 'd1e11546123bed6af17318bad4750772'
            }
        });
};

const searchCity = function(data){
    return {
        type: 'SEARCH_BY_CITY',
        data: data
    }
};