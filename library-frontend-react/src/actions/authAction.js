import { removeUserCookie, setUserCookie } from "../util/utils"

import { ROLE } from "../contants/global"
import authActions from "../services/authService"
import baseService from "../services/baseService"
import constants from "../contants/action_types/auth_constants"
import history from "../history"
import responseCodes from "../contants/responseCodes"
import urls from "../urls"

const onSignupSuccess = (dispatch, userData) => {
  setUserCookie(userData)
  baseService.addAuthTokenToHeader()
  dispatch({
    type: constants.SIGNUP_AUTHOR_SUCCESS
  })
  history.push(urls.home)
}

const authorSignupFailure = error => ({
  type: constants.SIGNUP_AUTHOR_FAILURE,
  payload: error
})

const publisherSignupFailure = error => ({
  type: constants.SIGNUP_PUBLISHER_FAILURE,
  payload: error
})

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
          dispatch({
            type: constants.LOGIN_SUCCESS
          })
          history.push(urls.home)
        } else {
          dispatch({
            type: constants.LOGIN_FAILURE,
            payload: response.data
          })
        }
      })
      .catch(error => {
        console.error(error)
        dispatch({
          type: constants.LOGIN_FAILURE,
          payload: error.response.data
        })
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
        console.error(error)
        dispatch({
          type: constants.LOGIN_FAILURE,
          payload: error.response.data
        })
      })
  }
}

export const authorSignup = formData => {
  return dispatch => {
    dispatch({ type: constants.SIGNUP_AUTHOR_STARTED })
    return authActions
      .signUpAuthor(formData)
      .then(response => {
        if (response.status === responseCodes.CREATED) {
          onSignupSuccess(dispatch, { ...response.data, role: ROLE.AUTHOR })
          history.push(urls.books)
        } else {
          dispatch(authorSignupFailure(response.data))
        }
      })
      .catch(error => {
        dispatch(authorSignupFailure(error.response.data))
      })
  }
}

export const publisherSignup = formData => {
  return dispatch => {
    dispatch({ type: constants.SIGNUP_PUBLISHER_STARTED })
    return authActions
      .signUpPublisher(formData)
      .then(response => {
        if (response.status === responseCodes.CREATED) {
          onSignupSuccess(dispatch, { ...response.data, role: ROLE.PUBLISHER })
          history.push(urls.books)
        } else {
          dispatch(publisherSignupFailure(response.data))
        }
      })
      .catch(error => {
        dispatch(publisherSignupFailure(error))
      })
  }
}
