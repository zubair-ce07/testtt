import CreateBlog from './presentation';
import CreateBlogContainer from './container';
import { TagsContainer } from '../tags';

export { CreateBlogReducer } from './reducer';

export default TagsContainer(CreateBlogContainer(CreateBlog));
