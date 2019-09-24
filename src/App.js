import React from 'react';
import UserLoginRegistrationForm from './UserComponents/LoginRegistrationForm/FormContainer';
import './App.css'

class App extends React.Component {
  render() {
    return (
        <div id='app' >
            <UserLoginRegistrationForm />
        </div>
    );
  }
}

export default App;
