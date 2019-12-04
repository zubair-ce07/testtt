import { createStore, applyMiddleware } from 'redux'
import { composeWithDevTools } from 'redux-devtools-extension/developmentOnly'
import thunkMiddleware from 'redux-thunk'
import promise from 'redux-promise-middleware'
import reducers from './reducers'

export default function configureStore (initialState = {}) {
  const store = createStore(
    reducers, initialState, composeWithDevTools(applyMiddleware(promise, thunkMiddleware)))
  return store
}
