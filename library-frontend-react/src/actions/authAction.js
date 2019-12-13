import { onErrorAction, removeUserCookie, setUserCookie } from "utils"

import { ROLE } from "constants/global"
import authActions from "services/authService"
import baseService from "services/baseService"
import constants from "constants/actionTypes/authConstants"
import history from "@history"
import urls from "urls"

const onSignupSuccess = (dispatch, userData) => {
  setUserCookie(userData)
  baseService.addAuthTokenToHeader()
  dispatch({ type: constants.SIGNUP_SUCCESS })
  history.push(urls.home)
}

// Sign in actions
export const signIn = formData => {
  return dispatch => {
    dispatch({ type: constants.LOGIN_STARTED })
    authActions
      .login(formData)
      .then(response => {
        setUserCookie(response.data)
        baseService.addAuthTokenToHeader()
        dispatch({ type: constants.LOGIN_SUCCESS })
        history.push(urls.home)
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
      .then(_response => {
        removeUserCookie()
        baseService.removeAuthToken()
        dispatch({ type: constants.LOGOUT_SUCCESS })
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
        onSignupSuccess(dispatch, { ...response.data, role: ROLE.AUTHOR })
        history.push(urls.books)
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
        onSignupSuccess(dispatch, { ...response.data, role: ROLE.PUBLISHER })
        history.push(urls.books)
      })
      .catch(error => {
        dispatch(onErrorAction(error, constants.SIGNUP_FAILURE))
      })
  }
}
