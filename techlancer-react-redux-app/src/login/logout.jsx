import { Redirect } from 'react-router-dom';
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import React from 'react';
import * as Actions from './actions.js'

class Logout extends React.Component {
	 componentWillMount() {
     this.props.actions.logout();
   }

	render() {
		return <Redirect to='/' />;
	}
}
function mapStateToProps(state) {
	return {}
}

function mapDispatchToProps(dispatch) {
  return {
    actions: bindActionCreators(Actions, dispatch)
  };
}
export default connect(
  mapStateToProps,
  mapDispatchToProps
)(Logout);
