import { connect } from 'react-redux';

import { load } from './actions';

const mapStateToProps = state => ({
  ...state.BlogDetailReducer,
  signedInUserId: state.UserReducer.user.id,
});

const mapDispatchToProps = dispatch => ({
  loadBlogDetail: blogId => dispatch(load(blogId)),
});

export default connect(mapStateToProps, mapDispatchToProps);
