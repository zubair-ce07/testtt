import { connect } from 'react-redux';

import { load } from './actions';

const mapStateToProps = state => ({
  tags: state.TagsReducer.tags
});

const mapDispatchToProps = dispatch => ({
  loadTags: () => dispatch(load()),
});

export default connect(mapStateToProps, mapDispatchToProps);
