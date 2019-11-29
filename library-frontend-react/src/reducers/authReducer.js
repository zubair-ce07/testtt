import constants from "../contants/action_types/auth_constants"
import { getUserCookie } from "../util/utils"

const initialState = {
  loading: false,
  currentUser: getUserCookie(),
  error: null
}

const authReducer = (state = initialState, action) => {
  switch (action.type) {
    case constants.SIGNUP_AUTHOR_STARTED:
      return { ...state, loading: true }
    case constants.LOGIN_SUCCESS:
      return { ...state, loading: false, currentUser: getUserCookie() }
    case constants.LOGOUT_SUCCESS:
      return { ...state, loading: false, currentUser: {} }
    case constants.SIGNUP_AUTHOR_SUCCESS:
      return {
        ...state,
        loading: false,
        error: false
      }
    case constants.SIGNUP_AUTHOR_FAILURE:
      return { ...state, error: action.payload, loading: false }
    default:
      return state
  }
}

export default authReducer
