import React from 'react';
import Container from '@material-ui/core/Container'
import AppSidebar from './SharedComponents/AppSidebar/AppSidebar'
import Profile from './UserComponents/Profile/Profile'
import './App.css';

const App = () => {
    return (
        <div className="App">
            <AppSidebar/>
            <Container>
                <Profile/>
            </Container>
        </div>
    );
};

export default App;
