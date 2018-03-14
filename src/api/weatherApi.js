


class weatherApi {
    static getWeatherData(name) {

        var url=`http://api.openweathermap.org/data/2.5/weather?q=London&appid=c6cfb5efbd67fc22c65db6bfc0514fdf`
        console.log(url)
        return fetch(url).then(response => {
            console.log(response)
            return response.json();
        }).catch(error => {
            console.log(error)
            return error;
        });
    }
}

    export default weatherApi;
