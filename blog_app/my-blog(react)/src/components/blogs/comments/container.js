import { connect } from 'react-redux';

import { load, addComment, addReply } from './actions';

const mapStateToProps = state => ({
  ...state.CommentsReducer,
  user: state.UserReducer.user,
});

const mapDispatchToProps = dispatch => ({
  loadComments: blogId => dispatch(load(blogId)),
  addComment: comment => dispatch(addComment(comment)),
  addReply: comment => dispatch(addReply(comment)),
});

export default connect(mapStateToProps, mapDispatchToProps);
