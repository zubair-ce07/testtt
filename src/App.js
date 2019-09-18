import React from 'react';
import './App.css';
import AppSidebar from './SharedComponents/AppSidebar/AppSidebar'
import Profile from './UserComponents/Profile/profile'
import Container from '@material-ui/core/Container'


function App() {
    return (
        <div className="App">
            <AppSidebar/>
            <Container>
                <Profile/>
            </Container>
        </div>
    );
}

export default App;
