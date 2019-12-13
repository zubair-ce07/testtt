import { PAGE_SIZE } from "constants/global"
import constants from "constants/actionTypes/authorConstants"
import { getPageNumberFromUrl } from "utils"

const initialState = {
  loading: false,
  authors: [],
  author: {},
  authorsData: [],
  error: null,

  next: null,
  previous: null,
  pagesCount: 1,
  totalCount: 0,
  currentPageNumber: 1
}

const authorsReducer = (state = initialState, action) => {
  switch (action.type) {
    case constants.FETCH_AUTHORS_STARTED:
    case constants.FETCH_AUTHOR_STARTED:
    case constants.FETCH_AUTHORS_DATA_STARTED:
      return {
        ...state,
        loading: true
      }

    case constants.SET_CURRENT_PAGE:
      return {
        ...state,
        currentPageNumber: action.payload
      }
    case constants.FETCH_AUTHORS_SUCCESS:
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

        authors: results
      }
    case constants.FETCH_AUTHORS_DATA_SUCCESS:
      return {
        ...state,
        loading: false,
        error: null,
        authorsData: action.payload
      }
    case constants.FETCH_AUTHOR_SUCCESS:
      return {
        ...state,
        loading: false,
        error: null,
        author: action.payload
      }

    case constants.FETCH_AUTHORS_FAILURE:
    case constants.FETCH_AUTHOR_FAILURE:
    case constants.FETCH_AUTHORS_DATA_FAILURE:
      return {
        ...state,
        loading: false,
        error: action.payload
      }
    default:
      return state
  }
}

export default authorsReducer
