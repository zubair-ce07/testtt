import { connect } from 'react-redux';

import {
  save, updateField, addTag, removeTag, load, reset
} from './actions';

const mapStateToProps = state => ({ ...state.CreateBlogReducer });

const mapDispatchToProps = dispatch => ({
  updateField: (name, value) => dispatch(updateField(name, value)),
  saveBlog: () => dispatch(save()),
  addTagToBlog: tag => dispatch(addTag(tag)),
  removeTagFromBlog: index => dispatch(removeTag(index)),
  loadBlog: blogId => dispatch(load(blogId)),
  resetBlog: () => dispatch(reset()),
});

export default connect(mapStateToProps, mapDispatchToProps);
