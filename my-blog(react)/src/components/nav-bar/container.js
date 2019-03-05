import { connect } from 'react-redux';

import { signOut, loadSignedInUser } from './actions';

const mapStateToProps = state => ({ ...state.UserReducer });

const mapDispatchToProps = dispatch => ({
  signOut: () => dispatch(signOut()),
  initialize: () => dispatch(loadSignedInUser()),
});

export default connect(mapStateToProps, mapDispatchToProps);
