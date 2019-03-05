import { connect } from 'react-redux';

import { signIn } from './actions';

const mapStateToProps = state => ({ ...state.UserReducer });

const mapDispatchToProps = dispatch => ({
  signIn: (username, password) => dispatch(signIn(username, password)),
});

export default connect(mapStateToProps, mapDispatchToProps);
