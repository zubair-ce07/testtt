import {
  FETCH_BOOKS_STARTED,
  FETCH_BOOKS_SUCCESS,
  FETCH_BOOKS_FAILURE
} from "../contants/action_types/book_constants"

import responseCodes from "../contants/responseCodes"
import urls from "../urls"
import history from "../history"

import { getBooks } from "../services/bookService"

export const getBooksList = searchQuery => {
  return dispath => {
    dispath({ type: FETCH_BOOKS_STARTED })
    getBooks(searchQuery)
      .then(response => {
        if (response.status === responseCodes.OK) {
          dispath({ type: FETCH_BOOKS_SUCCESS, payload: response.data })
        }
      })
      .catch(error => {
        dispatch({
          type: FETCH_BOOKS_FAILURE,
          payload: error.response.data
        })
        history.push(urls.login)
      })
  }
}
