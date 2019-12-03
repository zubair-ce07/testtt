import categoryService from "../services/categoryService"
import constants from "../contants/action_types/category_constants"
import { onErrorAction } from "../util/utils"
import responseCodes from "../contants/responseCodes"

export const setCurrentPage = pageNo => {
  return {
    type: constants.SET_CURRENT_PAGE,
    payload: pageNo
  }
}

export const getCategoriesList = searchQuery => {
  return dispatch => {
    dispatch({ type: constants.FETCH_CATEGORIES_STARTED })
    categoryService
      .getCategories(searchQuery)
      .then(response => {
        if (response.status === responseCodes.OK) {
          dispatch({
            type: constants.FETCH_CATEGORIES_SUCCESS,
            payload: response.data
          })
        }
      })
      .catch(error => {
        dispatch(onErrorAction(error, constants.FETCH_CATEGORIES_FAILURE))
      })
  }
}

export const getCategoriesDataList = () => {
  return dispatch => {
    dispatch({ type: constants.FETCH_CATEGORIES_DATA_STARTED })
    categoryService
      .getCategoriesData()
      .then(response => {
        if (response.status === responseCodes.OK) {
          dispatch({
            type: constants.FETCH_CATEGORIES_DATA_SUCCESS,
            payload: response.data
          })
        }
      })
      .catch(error => {
        dispatch(onErrorAction(error, constants.FETCH_CATEGORIES_DATA_FAILURE))
      })
  }
}

export const getCategoryDetail = categoryId => {
  return dispatch => {
    dispatch({ type: constants.FETCH_CATEGORY_STARTED })
    categoryService
      .getCategory(categoryId)
      .then(response => {
        if (response.status === responseCodes.OK) {
          dispatch({
            type: constants.FETCH_CATEGORY_SUCCESS,
            payload: response.data
          })
        }
      })
      .catch(error => {
        dispatch(onErrorAction(error, constants.FETCH_CATEGORY_FAILURE))
      })
  }
}
