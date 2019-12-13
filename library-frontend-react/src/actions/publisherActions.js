import constants from "constants/actionTypes/publisherConstants"
import { onErrorAction } from "utils"
import publisherService from "services/publisherService"

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
        dispatch({
          type: constants.FETCH_PUBLISHERS_DATA_SUCCESS,
          payload: response.data
        })
      })
      .catch(error => {
        dispatch(onErrorAction(error, constants.FETCH_PUBLISHERS_DATA_FAILURE))
      })
  }
}

export const getPublishersList = pageNo => {
  return dispatch => {
    dispatch({ type: constants.FETCH_PUBLISHERS_STARTED })
    publisherService
      .getPublishers(pageNo)
      .then(response => {
        dispatch({
          type: constants.FETCH_PUBLISHERS_SUCCESS,
          payload: response.data
        })
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
        dispatch({
          type: constants.FETCH_PUBLISHER_SUCCESS,
          payload: response.data
        })
      })
      .catch(error => {
        dispatch(onErrorAction(error, constants.FETCH_PUBLISHER_FAILURE))
      })
  }
}
