import constants from "../contants/action_types/publisher_constants"
import history from "../history"
import publisherService from "../services/publisherService"
import responseCodes from "../contants/responseCodes"
import urls from "../urls"

export const setCurrentPage = pageNo => {
  return {
    type: constants.SET_CURRENT_PAGE,
    payload: pageNo
  }
}

export const getPublishersDataList = () => {
  return dispatch => {
    dispatch({ type: constants.FETCH_PUBLISHERS_DATA_STARTED })
    publisherService
      .getPublishersData()
      .then(response => {
        if (response.status === responseCodes.OK) {
          dispatch({
            type: constants.FETCH_PUBLISHERS_DATA_SUCCESS,
            payload: response.data
          })
        }
      })
      .catch(error => {
        dispatch({
          type: constants.FETCH_PUBLISHERS_DATA_FAILURE,
          payload: error.response.data
        })
      })
  }
}

export const getPublishersList = pageNo => {
  return dispatch => {
    dispatch({ type: constants.FETCH_PUBLISHERS_STARTED })
    publisherService
      .getPublishers(pageNo)
      .then(response => {
        if (response.status === responseCodes.OK) {
          dispatch({
            type: constants.FETCH_PUBLISHERS_SUCCESS,
            payload: response.data
          })
        }
      })
      .catch(error => {
        dispatch({
          type: constants.FETCH_PUBLISHERS_FAILURE,
          payload: error
        })
      })
  }
}

export const getPublisherDetail = authorId => {
  return dispatch => {
    dispatch({ type: constants.FETCH_PUBLISHER_STARTED })
    publisherService
      .getPublisher(authorId)
      .then(response => {
        if (response.status === responseCodes.OK) {
          dispatch({
            type: constants.FETCH_PUBLISHER_SUCCESS,
            payload: response.data
          })
        }
      })
      .catch(error => {
        dispatch({
          type: constants.FETCH_PUBLISHER_FAILURE,
          payload: error
        })
        if (error.response.status === responseCodes.NOT_FOUND) {
          history.replace(urls.notFound)
        }
      })
  }
}
