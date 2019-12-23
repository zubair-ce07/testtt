import { LOGIN_USER, CURRENT_USER, UPDATE_USER } from './user.types'
import { fulfilled, pending } from 'helpers/api'
import { _exists } from 'helpers/common'

const initial = {
  user: {},
  userLoading: 0
}

export default function (state = initial, action) {
  switch (action.type) {
    case fulfilled(LOGIN_USER):
      return { ...state, user: _exists(action, 'payload.data.user', {}) }

    case pending(CURRENT_USER):
      return { ...state, userLoading: state.userLoading + 1 }
    case fulfilled(CURRENT_USER):
      return { ...state, user: _exists(action, 'payload.data', {}), userLoading: state.userLoading - 1 }

    case pending(UPDATE_USER):
      return { ...state, userLoading: state.userLoading + 1 }
    case fulfilled(UPDATE_USER):
      return { ...state, user: _exists(action, 'payload.data.data', state.user), userLoading: state.userLoading - 1 }
    default:
      return state
  }
}
