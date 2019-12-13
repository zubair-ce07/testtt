import { createStore, applyMiddleware } from "redux"
import rootReducer from "reducers/rootReducer"
import thunk from "redux-thunk"
import logger from "redux-logger"

const configureStore = () => {
  const store = createStore(rootReducer, applyMiddleware(thunk, logger))
  return store
}

export default configureStore
