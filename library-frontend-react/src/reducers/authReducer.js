import constants from "../contants/action_types/auth_constants"
import { getUserCookie } from "../util/utils"

const initialState = {
  loading: false,
  currentUser: getUserCookie(),
  error: null
}

const authReducer = (state = initialState, action) => {
  switch (action.type) {
    case constants.LOGIN_STARTED:
    case constants.LOGOUT_STARTED:
    case constants.SIGNUP_AUTHOR_STARTED:
      return { ...state, loading: true }

    case constants.SIGNUP_SUCCESS:
    case constants.LOGIN_SUCCESS:
      return { ...state, loading: false, currentUser: getUserCookie() }
    case constants.LOGOUT_SUCCESS:
      return { ...state, loading: false, currentUser: {} }

    case constants.LOGIN_FAILURE:
      const { non_field_errors } = action.payload
      const err = non_field_errors ? non_field_errors : action.payload
      return { ...state, error: err, loading: false }
    case constants.LOGOUT_FAILURE:
    case constants.SIGNUP_FAILURE:
      return { ...state, error: action.payload, loading: false }
    default:
      return state
  }
}

export default authReducer
