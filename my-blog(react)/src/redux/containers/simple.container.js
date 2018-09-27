import { connect } from 'react-redux';
import { simpleAction } from '../actions/simple.action';

const mapStateToProps = state => ({
  ...state
});

const mapDispatchToProps = dispatch => ({
  simpleAction: () => dispatch(simpleAction())
});


export default connect(mapStateToProps, mapDispatchToProps);
