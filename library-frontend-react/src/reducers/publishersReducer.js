import { PAGE_SIZE } from "constants/global"
import constants from "constants/actionTypes/publisherConstants"
import { getPageNumberFromUrl } from "utils"

const initialState = {
  loading: false,
  publishers: [],
  publisher: {},
  publishersData: [],
  error: null
}

const publishersReducer = (state = initialState, action) => {
  switch (action.type) {
    case constants.FETCH_PUBLISHERS_STARTED:
    case constants.FETCH_PUBLISHER_STARTED:
    case constants.FETCH_PUBLISHERS_DATA_STARTED:
      return {
        ...state,
        loading: true
      }

    case constants.FETCH_AUTHORS_DATA_STARTED:
      return {
        ...state,
        loading: true
      }

    case constants.FETCH_PUBLISHERS_SUCCESS:
      const { count, next, previous, results } = action.payload

      const nextPageNo = getPageNumberFromUrl(next)
      const prevPageNo = getPageNumberFromUrl(previous)

      let totalPages = Math.ceil(count / PAGE_SIZE)

      return {
        ...state,
        loading: false,
        error: null,

        totalCount: count,
        pagesCount: totalPages,
        next: nextPageNo,
        previous: prevPageNo,

        publishers: results
      }
    case constants.FETCH_PUBLISHERS_DATA_SUCCESS:
      return {
        ...state,
        loading: false,
        error: null,
        publishersData: action.payload
      }
    case constants.FETCH_PUBLISHER_SUCCESS:
      return {
        ...state,
        loading: false,
        error: null,
        publisher: action.payload
      }

    case constants.FETCH_PUBLISHERS_DATA_FAILURE:
    case constants.FETCH_PUBLISHERS_FAILURE:
    case constants.FETCH_PUBLISHER_FAILURE:
      return {
        ...state,
        loading: false,
        error: action.payload
      }
    default:
      return state
  }
}

export default publishersReducer
