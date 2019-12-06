import { LOGIN_USER, CURRENT_USER, UPDATE_USER } from './user.types'
import { fulfilled } from 'helpers/api'
import { _exists } from 'helpers/common'

const initial = {
  user: {}
}

export default function (state = initial, action) {
  switch (action.type) {
    case fulfilled(LOGIN_USER):
      return { ...state, user: _exists(action, 'payload.data.user', {}) }
    case fulfilled(CURRENT_USER):
      return { ...state, user: _exists(action, 'payload.data', {}) }
    case fulfilled(UPDATE_USER):
      return { ...state, user: _exists(action, 'payload.data.data', state.user) }
    default:
      return state
  }
}
