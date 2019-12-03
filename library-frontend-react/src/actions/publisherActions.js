import constants from "../contants/action_types/publisher_constants"
import history from "../history"
import { onErrorAction } from "../util/utils"
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
        const response = error.response

        dispatch({
          type: constants.FETCH_PUBLISHERS_DATA_FAILURE,
          payload: response ? response.data : error
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
        dispatch(onErrorAction(error, constants.FETCH_PUBLISHERS_FAILURE))
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
        const response = error.response
        dispatch(onErrorAction(error, constants.FETCH_PUBLISHER_FAILURE))

        if (response && response.status === responseCodes.NOT_FOUND) {
          history.replace(urls.notFound)
        }
      })
  }
}
