import React, {Component} from 'react';
import { browserHistory} from 'react-router';
import {connect} from 'react-redux';
import {bindActionCreators} from 'redux';
import {getUserProfile} from '../actions'

class UserProfile extends Component {
     componentWillMount(){
        if (localStorage.getItem('token')) {
             this.props.getUserProfile(this.props.params.id, localStorage.getItem('token'));
        }
        else {
            browserHistory.push('/');
        }
    }
    checkStatus(){
         if (this.props.user)
         { return (
             <div className="row col-md-8 col-md-offset-2">
                  <center><h2> <b>Your Profile</b> </h2></center> <br/>
                 <div className="col-md-4 col-md-offset-2">
                     <img src={this.props.user.image} alt="" height="200px" width="200px"/>
                 </div>
                 <div className="col-md-4 col-md-offset-1">
                     <h4><b>{ this.props.user.first_name } {this.props.user.last_name }</b></h4>
                        <i className="fa fa-user fa-fw"></i> <b>{ this.props.user.username }</b>
                                <p>
                                    <i className="fa fa-envelope fa-fw"></i> <b>{this.props.user.email }</b>
                                    <br />
                                    </p>

                                <div className="btn-group">
                                   <a href={'editprofile'+this.props.user.id}> <button type="button"  className="btn btn-primary"> Edit Profile  </button></a>
                                </div>
                 </div>

             </div>
             );
         }
        return (
                <strong> Loading... </strong>
            ) ;

    }

    render() {
        return (      <div>{this.checkStatus()} </div>   );
    }
}



function mapStateToProps(state){
   return {
       user:state.user
   };
}
function mapDispatchToProps(dispatch){
    return bindActionCreators(
        {
            getUserProfile: getUserProfile
        }, dispatch);
}

export default connect(mapStateToProps, mapDispatchToProps)(UserProfile)