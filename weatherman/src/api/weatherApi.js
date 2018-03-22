
class weatherApi {
    static getWeatherData(name) {

        var url='http://api.openweathermap.org/data/2.5/forecast?q='+name+'&appid=c6cfb5efbd67fc22c65db6bfc0514fdf';
        return fetch(url).then(response => {
            return response.json();
        }).catch(error => {
            return error;
        });
    }
}

export default weatherApi;
