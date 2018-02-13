import React, {Component} from 'react';
import {connect} from 'react-redux';

class User extends Component {
    render() {
        if (!this.props.user) {
            return (<h4> Select a user to see details </h4>);
        }
        return (
          <div>
              <img src={this.props.user.thumbnail}/>
              <h4> {this.props.user.first} {this.props.user.last} </h4>
              <h5> Description: {this.props.user.description}</h5>
              <h5> Age: {this.props.user.age}</h5>
          </div>
        );
    };
};

function mapStateTOProps(state){
  return {  user: state.selectedUser};
}

export default connect(mapStateTOProps)(User);