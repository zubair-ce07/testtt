import authorService from "services/authorService"
import constants from "constants/actionTypes/authorConstants"
import { onErrorAction } from "utils"

export const setCurrentPage = pageNo => {
  return {
    type: constants.SET_CURRENT_PAGE,
    payload: pageNo
  }
}

export const getAuthorsDataList = () => {
  return dispatch => {
    dispatch({ type: constants.FETCH_AUTHORS_DATA_STARTED })
    return authorService
      .getAuthorsData()
      .then(response => {
        dispatch({
          type: constants.FETCH_AUTHORS_DATA_SUCCESS,
          payload: response.data
        })
      })
      .catch(error => {
        dispatch(onErrorAction(error, constants.FETCH_AUTHORS_DATA_FAILURE))
      })
  }
}

export const getAuthorsList = pageNo => {
  return dispatch => {
    dispatch({ type: constants.FETCH_AUTHORS_STARTED })
    authorService
      .getAuthors(pageNo)
      .then(response => {
        dispatch({
          type: constants.FETCH_AUTHORS_SUCCESS,
          payload: response.data
        })
      })
      .catch(error => {
        dispatch(onErrorAction(error, constants.FETCH_AUTHORS_FAILURE))
      })
  }
}

export const getAuthorDetail = authorId => {
  return dispatch => {
    dispatch({ type: constants.FETCH_AUTHOR_STARTED })
    authorService
      .getAuthor(authorId)
      .then(response => {
        dispatch({
          type: constants.FETCH_AUTHOR_SUCCESS,
          payload: response.data
        })
      })
      .catch(error => {
        dispatch(onErrorAction(error, constants.FETCH_AUTHOR_FAILURE))
      })
  }
}
