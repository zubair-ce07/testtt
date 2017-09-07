import React from 'react';
import WeatherCharList from '../containers/weither-chart-list';
import SearchWeather from '../containers/search-weather';

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

