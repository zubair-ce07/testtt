import { LOGIN_USER, CURRENT_USER } from './user.types'
import { fulfilled } from 'helpers/api'

const initial = {
  user: {}
}

export default function (state = initial, action) {
  switch (action.type) {
    case fulfilled(LOGIN_USER):
      return { ...state, user: action.payload.data.user }
    case fulfilled(CURRENT_USER):
      return { ...state, user: action.payload.data }
    default:
      return state
  }
}
