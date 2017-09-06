import React from 'react';
import UserList from '../containers/user-list'
import User from '../containers/user'
import AddUser from '../containers/add-user'

const App =  function(){
    return (
        <div>
            <AddUser />
            <h2>List Of Users</h2>
            <hr/>
            <UserList/>
            <h2>User Detail</h2>
            <hr/>
            <User/>
        </div>

    );
};
export default App;
