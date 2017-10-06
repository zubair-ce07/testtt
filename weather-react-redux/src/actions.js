import axios from 'axios';

export const search = query => {

    console.log(query);

    return function (dispatch) {
        axios.get('http://api.openweathermap.org/data/2.5/forecast?q=' + query + '&units=metric&appid=7e7472adf234ce0d2a91699296939c2a')
            .then((respone) => {
                dispatch({ type: 'WEATHER_UPDATE', payload: respone.data })

            })
            .catch((err) => {
                console.log(err);
            })
    }

};
