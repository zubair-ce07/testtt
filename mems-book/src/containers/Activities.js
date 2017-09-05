import React, {Component} from 'react';
import { browserHistory} from 'react-router';
import {connect} from 'react-redux';
import {bindActionCreators} from 'redux';
import {getUserActivities} from '../actions'
import Activity from '../components/Activity'

class UserMems extends Component {
     componentWillMount(){
        if (localStorage.getItem('token')) {
             this.props.getUserActivities(localStorage.getItem('token'));
        }
        else {
            browserHistory.push('/');
        }
    }
     renderActivities() {
        return this.props.user_activities.map((activity)=>
                    { return <Activity key={activity.id} activity={activity}/> });
    }
    render() {
        return (

            <div className="well">
               <center><h2> <b>Your Activities</b> </h2></center> <br/>

                <ul className="list-group">
                    {this.renderActivities()}
                </ul>


          </div>
        );
    }
}



function mapStateToProps(state){

   return {
       user_activities:state.user_activities
   };
}
function mapDispatchToProps(dispatch){
    return bindActionCreators(
        {
            getUserActivities: getUserActivities
        }, dispatch);
}

export default connect(mapStateToProps, mapDispatchToProps)(UserMems)







