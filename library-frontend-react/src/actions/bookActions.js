import bookService from "services/bookService"
import constants from "constants/actionTypes/bookConstants"
import history from "@history"
import { onErrorAction } from "utils"
import urls from "urls"

export const setCurrentPage = pageNo => {
  return {
    type: constants.SET_CURRENT_PAGE,
    payload: pageNo
  }
}

export const clearBookData = () => {
  return { type: constants.ClEAR_BOOK_DATA }
}

export const getBooksList = pageNo => {
  return dispatch => {
    dispatch({ type: constants.FETCH_BOOKS_STARTED })
    bookService
      .getBooks(pageNo)
      .then(response => {
        dispatch({
          type: constants.FETCH_BOOKS_SUCCESS,
          payload: response.data
        })
      })
      .catch(error => {
        dispatch(onErrorAction(error, constants.FETCH_BOOKS_FAILURE))
      })
  }
}

export const getBookDetail = bookId => {
  return dispatch => {
    dispatch({ type: constants.FETCH_BOOK_STARTED })
    bookService
      .getBook(bookId)
      .then(response => {
        dispatch({
          type: constants.FETCH_BOOK_SUCCESS,
          payload: response.data
        })
      })
      .catch(error => {
        dispatch(onErrorAction(error, constants.FETCH_BOOK_FAILURE))
      })
  }
}

export const createBook = bookData => {
  return dispatch => {
    dispatch({ type: constants.CREATE_BOOK_STARTED })
    return bookService
      .newBook(bookData)
      .then(response => {
        dispatch({
          type: constants.CREATE_BOOK_SUCCESS,
          payload: response.data
        })
        history.push(`${urls.book}${response.data.id}`)
      })
      .catch(error => {
        dispatch(onErrorAction(error, constants.CREATE_BOOK_FAILURE))
      })
  }
}

export const updateBookDetails = (bookId, bookData) => {
  return dispatch => {
    dispatch({ type: constants.UPDATE_BOOK_STARTED })
    return bookService
      .updateBook(bookId, bookData)
      .then(response => {
        dispatch({
          type: constants.UPDATE_BOOK_SUCCESS,
          payload: response.data
        })
        history.push(`${urls.book}${bookId}`)
      })
      .catch(error => {
        dispatch(onErrorAction(error, constants.UPDATE_BOOK_FAILURE))
      })
  }
}

export const deleteBook = bookId => {
  return dispatch => {
    dispatch({ type: constants.DELETE_BOOK_STARTED })
    bookService
      .oremoveBook(bookId)
      .then(response => {
        dispatch({
          type: constants.DELETE_BOOK_SUCCESS,
          payload: bookId
        })
        history.push(urls.books)
      })
      .catch(error => {
        dispatch(onErrorAction(error, constants.DELETE_BOOK_FAILURE))
      })
  }
}
