import {combineReducers} from 'redux';
import users from './users';
import selectedUser from './seleted-user'

const allReducers = combineReducers({
    users,
    selectedUser
});
export default allReducers;