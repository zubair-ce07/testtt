import { connect } from 'react-redux';

import { save, updateField, matchPassword } from './actions';

const mapStateToProps = state => ({ ...state.UserReducer });

const mapDispatchToProps = dispatch => ({
  updateField: (name, value, required) =>
    dispatch(updateField(name, value, required)),
  matchPassword: () => dispatch(matchPassword()),
  save: () => dispatch(save()),
});

export default connect(mapStateToProps, mapDispatchToProps);
