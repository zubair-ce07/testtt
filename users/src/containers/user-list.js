import React, {Component} from 'react';
import {connect} from 'react-redux';
import {bindActionCreators} from 'redux';
import {selectUser} from '../actions';

class UserList extends Component{

    render(){
        const users = this.props.users.map(user => {
           return  (
            <div>

               <li
                   key={user.id}
                   onClick={e => {
                       e.preventDefault();
                       this.props.selectUser(user);
                   }}
               >
                   {user.first} {user.last}
               </li>
            </div>
           );
        });
      return (
          <ul>
            {users}
          </ul>
      );
    }
};

function mapStateTOProps(state){
    return {
      users:state.users
    };
};
function mapDispatchToProps(dispatch){
    return bindActionCreators({selectUser: selectUser}, dispatch);
}
export default connect(mapStateTOProps, mapDispatchToProps)(UserList);

