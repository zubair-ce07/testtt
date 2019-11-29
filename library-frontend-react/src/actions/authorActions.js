import authorService from "../services/authorService"
import constants from "../contants/action_types/author_constants"
import history from "../history"
import responseCodes from "../contants/responseCodes"
import urls from "../urls"

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
        if (response.status === responseCodes.OK) {
          dispatch({
            type: constants.FETCH_AUTHORS_DATA_SUCCESS,
            payload: response.data
          })
        }
      })
      .catch(error => {
        dispatch({
          type: constants.FETCH_AUTHORS_DATA_FAILURE,
          payload: error.response.data
        })
      })
  }
}

export const getAuthorsList = pageNo => {
  return dispatch => {
    dispatch({ type: constants.FETCH_AUTHORS_STARTED })
    authorService
      .getAuthors(pageNo)
      .then(response => {
        if (response.status === responseCodes.OK) {
          dispatch({
            type: constants.FETCH_AUTHORS_SUCCESS,
            payload: response.data
          })
        }
      })
      .catch(error => {
        dispatch({
          type: constants.FETCH_AUTHORS_FAILURE,
          payload: error
        })
      })
  }
}

export const getAuthorDetail = authorId => {
  return dispatch => {
    dispatch({ type: constants.FETCH_AUTHOR_STARTED })
    authorService
      .getAuthor(authorId)
      .then(response => {
        if (response.status === responseCodes.OK) {
          dispatch({
            type: constants.FETCH_AUTHOR_SUCCESS,
            payload: response.data
          })
        }
      })
      .catch(error => {
        dispatch({
          type: constants.FETCH_AUTHOR_FAILURE,
          payload: error
        })
        if (error.response.status === responseCodes.NOT_FOUND) {
          history.replace(urls.notFound)
        }
      })
  }
}
