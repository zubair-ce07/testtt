import { connect } from 'react-redux';

import { load } from './actions';

const mapStateToProps = state => ({ ...state.BlogsListReducer });

const mapDispatchToProps = dispatch => ({
  loadBlogs: () => dispatch(load()),
});

export default connect(mapStateToProps, mapDispatchToProps);
