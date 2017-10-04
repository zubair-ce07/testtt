import React from 'react';
import WeatherChartList from '../containers/WeatherChartList';
import SearchBox from '../containers/SearchBox.js';

const App = function(){
    return (
        <div>
            <div>
                <SearchBox/>
            </div>
            <div>
                <WeatherChartList />
            </div>
        </div>
    );
};
export default App;

