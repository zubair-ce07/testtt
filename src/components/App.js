// App.js

import React from 'react';
import Search from '../containers/Search';
import Visualization from '../containers/Visualization';

const App = () => {
    return (
        <div className="container">
            <Search></Search>
            <Visualization></Visualization>
        </div>
    )
}
export default App;