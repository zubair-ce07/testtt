import { FETCH_WEATHER } from '../config'


export default function(state={weather_data: [], error: ''}, action)
{
    switch (action.type)
    {
        case FETCH_WEATHER:
            if(action.payload.data)
                /*
                    Check whether certain city
                    weather data exists
                */
                return { weather_data: [ action.payload.data ].concat(state.weather_data), error: '' };
            else
                return { weather_data: state.weather_data , error: "Weather Data not found" };
    }
    return state;
}