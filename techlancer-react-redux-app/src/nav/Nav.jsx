import React from 'react';
import {connect} from 'react-redux';
import {bindActionCreators} from 'redux';
import PropTypes from 'prop-types';
import * as Actions from './action.jsx'
// import Auth from '../services/auth.jsx';
import NavHeader from './Nav_header'
import Menu from './Menu'
import FreelancerMenu from './freelancer/Menu.jsx';


class Nav extends React.Component {
    componentWillMount() {
     this.props.actions.fetchUser();
   }
   componentWillUpdate(nextProps, nextState){
    if(nextProps.state.login_reducer.token !== this.props.state.login_reducer.token)
    {
      this.props.actions.fetchUser();
    }
   }
   static propTypes =  {
                          actions: PropTypes.object,
                          state: PropTypes.object
                        };
    menu(){
      if(this.props.state.nav_reducer.user+"" !== "")
      {
        return (<FreelancerMenu/>)
      }
      else
      {
        return(<Menu/>)
      }
    }

    render() {
        return (
            <nav className="navbar navbar-default" role="navigation">
                <div className="container">
                    <NavHeader />
                    {this.menu()}
                 <div className="clearfix"> </div>
                </div>
            </nav>
        );
    }
}
function mapStateToProps(state) {
  return {
    state: state
  };
}

function mapDispatchToProps(dispatch) {
  return {
    actions: bindActionCreators(Actions, dispatch)
  };
}
export default connect(
  mapStateToProps,
  mapDispatchToProps
)(Nav);
