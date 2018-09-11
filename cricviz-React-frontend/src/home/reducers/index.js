import { combineReducers } from 'redux';
import TeamsReducer from './reducer_Teams';

const rootReducer = combineReducers({
  teams: TeamsReducer
});

export default rootReducer;
