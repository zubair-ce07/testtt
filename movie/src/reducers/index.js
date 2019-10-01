import { combineReducers } from "redux";
import authReducer from "./authReducer";
import userReducer from "./userReducer";
import formReducer from "./formReducer";

const rootReducer = combineReducers({
  authReducer,
  userReducer,
  formReducer
});

export default rootReducer;
