import _ from 'lodash';
import React from 'react';
import UserCard from './user_item';


export const UserList = ({users}) => {
    return <div>{renderUsers(users)}</div>
};

const renderUsers = (users) => {
    return _.map(users, user => {
        return (
            <div className="mt-4" key={user.id}>
                <UserCard user_profile={user} show_actions={false}/>
            </div>
        );
    });
};
