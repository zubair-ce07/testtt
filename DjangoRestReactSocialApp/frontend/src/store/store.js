import { createStore, applyMiddleware } from 'redux'
import { composeWithDevTools } from 'redux-devtools-extension/developmentOnly'
import thunkMiddleware from 'redux-thunk'
import promise from 'redux-promise-middleware'
import reduxWebsocket from 'react-redux-websocket'
import reducers from './reducers'

import { isLogin, getUser } from 'helpers/auth'

const SOCKET_URL = process.env.REACT_APP_SOCKET_URL
let socket
if (isLogin()) {
  const user = getUser()
  socket = new WebSocket(`${SOCKET_URL}/${user.username}`)
} else {
  socket = new WebSocket(`${SOCKET_URL}/dummy`)
}

const socketIoMiddleware = reduxWebsocket(socket)

export default function configureStore (initialState = {}) {
  const store = createStore(
    reducers, initialState, composeWithDevTools(applyMiddleware(promise, thunkMiddleware, socketIoMiddleware)))
  return store
}
