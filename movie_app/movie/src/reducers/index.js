import { combineReducers } from "redux";
import authReducer from "./authReducer";
import formReducer from "./formReducer";

const rootReducer = combineReducers({
  authReducer,
  formReducer
});

export default rootReducer;
