import { createStore, applyMiddleware, compose } from "redux";
import thunk from "redux-thunk";
import rootReducer from "../reducers";

const saveToLocalStorage = state => {
  try {
    const serializedState = JSON.stringify(state);
    localStorage.setItem("state", serializedState);
  } catch (e) {
    return;
  }
};

const loadFromLocalStorage = () => {
  try {
    const serializedState = localStorage.getItem("state");
    if (serializedState === null) return;
    return JSON.parse(serializedState);
  } catch (e) {
    return;
  }
};

const persistedState = loadFromLocalStorage();
const store = createStore(
  rootReducer,
  persistedState,
  compose(applyMiddleware(thunk))
);
store.subscribe(() => saveToLocalStorage(store.getState()));

export { store };
