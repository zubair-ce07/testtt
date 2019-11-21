import {
  SIGNUP_AUTHOR_STARTED,
  SIGNUP_AUTHOR_SUCCESS,
  SIGNUP_AUTHOR_FAILURE
} from "../contants/action_types/auth_constants"

const initialState = {
  userData: {},
  loading: false,
  error: null
}

const authReducer = (state = initialState, action) => {
  switch (action.type) {
    case SIGNUP_AUTHOR_STARTED:
      return { ...state, isFetching: true }
    case SIGNUP_AUTHOR_SUCCESS:
      return {
        ...state,
        userData: action.payload,
        loading: false,
        error: false
      }
    case SIGNUP_AUTHOR_FAILURE:
      return { ...state, error: action.payload, loading: false }
    default:
      return state
  }
}

export default authReducer
