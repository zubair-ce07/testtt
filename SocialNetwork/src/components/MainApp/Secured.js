import React from 'react';
import PostList from '../Post/PostList'
import FriendList from '../Friend/FriendList'
import UserList from '../Users/UserList'

const Secured = () => {
        return(
            <div className="container-fluid">
                <div className="row">
                    <div className="col-lg-3">
                        <h3 style={{textAlign: "center"}} >Search for friends </h3>
                        <UserList />
                    </div>
                    <div className="col-lg-6">
                        <h3 style={{textAlign: "center"}} >News Feed</h3>
                        <PostList />    
                    </div>
                    <div className="col-lg-3">
                        <h3 style={{textAlign: "center"}} >Friends</h3>
                        <FriendList />                      
                    </div>
                </div>
            </div>
        );
}

export default Secured;