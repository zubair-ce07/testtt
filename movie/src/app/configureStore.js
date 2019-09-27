import {createStore, applyMiddleware, compose} from "redux";
import thunk from "redux-thunk";
import rootReducer from "../reducers";

// const rootReducer = combineReducers(loginReducer);
// const initailState = {
//     loading: false,
//     user: null,
//     error: null
//   };

const store = createStore(rootReducer, compose(applyMiddleware(thunk)));

export {store};
