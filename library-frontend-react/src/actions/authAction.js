import { onErrorAction, removeUserCookie, setUserCookie } from "../util/utils"

import { ROLE } from "../contants/global"
import authActions from "../services/authService"
import baseService from "../services/baseService"
import constants from "../contants/action_types/auth_constants"
import history from "../history"
import responseCodes from "../contants/responseCodes"
import urls from "../urls"

const onSignupSuccess = (dispatch, userData, type) => {
  setUserCookie(userData)
  baseService.addAuthTokenToHeader()
  dispatch({ type: type })
  history.push(urls.home)
}

// Sign in actions
export const signIn = formData => {
  return dispatch => {
    dispatch({ type: constants.LOGIN_STARTED })
    authActions
      .login(formData)
      .then(response => {
        if (response.status === responseCodes.OK) {
          setUserCookie(response.data)
          baseService.addAuthTokenToHeader()
          dispatch({ type: constants.LOGIN_SUCCESS })
          history.push(urls.home)
        } else {
          dispatch({
            type: constants.LOGIN_FAILURE,
            payload: response.data
          })
        }
      })
      .catch(error => {
        dispatch(onErrorAction(error, constants.LOGIN_FAILURE))
      })
  }
}

export const signOut = () => {
  return dispatch => {
    dispatch({ type: constants.LOGOUT_STARTED })
    authActions
      .logout()
      .then(response => {
        if (response.status === responseCodes.OK) {
          removeUserCookie()
          baseService.removeAuthToken()
          dispatch({
            type: constants.LOGOUT_SUCCESS
          })
        } else {
        }
      })
      .catch(error => {
        dispatch(onErrorAction(error, constants.LOGOUT_FAILURE))
      })
  }
}

export const authorSignup = formData => {
  return dispatch => {
    dispatch({ type: constants.SIGNUP_STARTED })
    return authActions
      .signUpAuthor(formData)
      .then(response => {
        if (response.status === responseCodes.CREATED) {
          onSignupSuccess(
            dispatch,
            { ...response.data, role: ROLE.AUTHOR },
            constants.SIGNUP_SUCCESS
          )
          history.push(urls.books)
        } else {
          dispatch(onErrorAction(response.data, constants.SIGNUP_FAILURE))
        }
      })
      .catch(error => {
        dispatch(onErrorAction(error, constants.SIGNUP_FAILURE))
      })
  }
}

export const publisherSignup = formData => {
  return dispatch => {
    dispatch({ type: constants.SIGNUP_STARTED })
    return authActions
      .signUpPublisher(formData)
      .then(response => {
        if (response.status === responseCodes.CREATED) {
          onSignupSuccess(
            dispatch,
            { ...response.data, role: ROLE.PUBLISHER },
            constants.SIGNUP_SUCCESS
          )
          history.push(urls.books)
        } else {
          dispatch(onErrorAction(response.data, constants.SIGNUP_FAILURE))
        }
      })
      .catch(error => {
        dispatch(onErrorAction(error, constants.SIGNUP_FAILURE))
      })
  }
}
