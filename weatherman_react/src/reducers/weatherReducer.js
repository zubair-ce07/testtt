export function monthlyWeather (state=null, action) {

    switch (action.type) {
        case 'FETCH_MONTHLY_WEATHER_SUCCEEDED':
            state = action.payload;
            break;
        case 'RESET_MONTHLY_WEATHER':
            state = null;
            break;
    }

    return state;

}

export function yearlyWeather (state=null, action) {
    switch (action.type) {
        case 'FETCH_YEARLY_WEATHER_SUCCEEDED':
            state = action.payload;
            break;
        case 'RESET_YEARLY_WEATHER':
            state=null;
            break;

    }

    return state;

}