import React from 'react';
import './App.css';
import NewsFeed from './PostComponents/NewsFeed';
import AppSidebar from './SharedComponents/AppSidebar/AppSidebar';

const App = () => {
    return (
        <div className="App">
            <AppSidebar/>
            <NewsFeed/>
        </div>
    );
};

export default App;
