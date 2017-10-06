const allReducers = function (state = { weatherList: [] }, action) {
    switch (action.type) {
        case 'WEATHER_UPDATE':
            return Object.assign({}, state, {
                weatherList: state.weatherList.concat(action.payload),
            });
        default:
            return state;
    }
};


export default allReducers;