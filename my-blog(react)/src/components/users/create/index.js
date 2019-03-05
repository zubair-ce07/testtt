import CreateUser from './presentation';
import CreateUserContainer from './container';

export { UserReducer } from './reducer';

export default CreateUserContainer(CreateUser);
