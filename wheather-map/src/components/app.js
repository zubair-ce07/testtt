import React from 'react';
import WeatherCharList from '../containers/weitherCharList';
import SearchWeather from '../containers/searchWeather';

const App = function(){
    return (
        <div>
            <SearchWeather/>
            <hr/>
            <WeatherCharList />
        </div>
    );
};
export default App;

