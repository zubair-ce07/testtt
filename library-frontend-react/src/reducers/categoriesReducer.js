import { PAGE_SIZE } from "../contants/global"
import constants from "../contants/action_types/category_constants"
import { getPageNumberFromUrl } from "../util/utils"

const initialState = {
  loading: false,
  categories: [],
  categoriesData: [],
  category: {},
  error: null,

  next: null,
  previous: null,
  pagesCount: 1,
  totalCount: 0,
  currentPageNumber: 1
}

const categoriesReducer = (state = initialState, action) => {
  switch (action.type) {
    case constants.FETCH_CATEGORIES_STARTED:
    case constants.FETCH_CATEGORY_STARTED:
    case constants.FETCH_CATEGORIES_DATA_STARTED:
      return {
        ...state,
        loading: true
      }

    case constants.FETCH_CATEGORIES_SUCCESS:
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

        categories: results
      }
    case constants.FETCH_CATEGORIES_DATA_SUCCESS:
      return {
        ...state,
        loading: false,
        error: null,
        categoriesData: action.payload
      }
    case constants.FETCH_CATEGORY_SUCCESS:
      return {
        ...state,
        loading: false,
        error: null,
        category: action.payload
      }

    case constants.FETCH_CATEGORIES_DATA_FAILURE:
    case constants.FETCH_CATEGORIES_FAILURE:
    case constants.FETCH_CATEGORY_FAILURE:
      return {
        ...state,
        loading: false,
        error: action.payload
      }
    default:
      return state
  }
}

export default categoriesReducer
