import React, {Component} from 'react';
import { browserHistory} from 'react-router';
import {connect} from 'react-redux';
import {bindActionCreators} from 'redux';
import {getPublicMems} from '../actions'
import Memory from '../components/Mem'

class PublicMems extends Component {
     componentWillMount(){
        if (localStorage.getItem('token')) {
             this.props.getPublicMems(localStorage.getItem('token'));
        }
        else {
            browserHistory.push('/');
        }
    }
     renderAllMems() {
        return this.props.public_mems.map((mem)=> { return <Memory key={mem.id} mem={mem}/> });
    }
    render() {
        return (

          <div>
              <center><h2> <b>Public Mems</b> </h2></center> <br/>
            {this.renderAllMems()}
            </div>
        );
    }
}



function mapStateToProps(state){

   return {
       public_mems:state.public_mems
   };
};
function mapDispatchToProps(dispatch){
    return bindActionCreators(
        {
            getPublicMems: getPublicMems
        }, dispatch);
};

export default connect(mapStateToProps, mapDispatchToProps)(PublicMems);
