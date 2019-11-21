import {
  SIGNUP_AUTHOR_STARTED,
  SIGNUP_AUTHOR_SUCCESS,
  SIGNUP_AUTHOR_FAILURE
} from "../contants/action_types/auth_constants"

import responseCodes from "../contants/responseCodes"
import urls from "../urls"
import history from "../history"

import baseService from "../services/baseService"
import { signUpAuthor } from "../services/authService"
import { setCookieAuthToken } from "../util/utils"

// import Notification from '';

const onLoginSuccess = (dispatch, response) => {
  setCookieAuthToken(response.data.token)
  baseService.addAuthTokenToHeader()
  dispatch({
    type: SIGNUP_AUTHOR_SUCCESS,
    payload: response.data
  })
  history.push(urls.home)
}

const authorSignupFailure = error => ({
  type: SIGNUP_AUTHOR_FAILURE,
  payload: error
})

// // Sign in actions
// export const signIn = formData => {
//   return dispatch => {
//     dispatch({ type: authConstants.SIGN_IN });
//     authService.login({ ...formData }).then(response => {
//       if (response.status === responseCodes.OK) {
//         onLoginSuccess(dispatch, response);
//       } else {
//         // Notification.error(response.data.error);
//       }
//     });
//   };
// };

export const authorSignup = formData => {
  return dispatch => {
    dispatch({ type: SIGNUP_AUTHOR_STARTED })
    signUpAuthor({ formData })
      .then(response => {
        if (response.status === responseCodes.CREATED) {
          onLoginSuccess(dispatch, response)
        } else {
          dispatch(authorSignupFailure(response.data))
          // Notification.error(error);
        }
      })
      .catch(error => {
        dispatch(authorSignupFailure(error.response.data))
      })
  }
}

// export const publisherSignup = formData => {
//   return dispatch => {
//     dispatch({ type: authConstants.SIGN_UP });
//     signUpAuthor({ ...formData }).then(response => {
//       if (response.data.response_code === responseCodes.OK) {
//         onLoginSuccess(dispatch, response);
//       } else {
//         // Notification.error(response.data.error);
//       }
//     });
//   };
// };
