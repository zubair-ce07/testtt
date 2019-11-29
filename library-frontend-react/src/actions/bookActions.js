import bookService from "../services/bookService"
import constants from "../contants/action_types/book_constants"
import history from "../history"
import responseCodes from "../contants/responseCodes"
import urls from "../urls"

export const setCurrentPage = pageNo => {
  return {
    type: constants.SET_CURRENT_PAGE,
    payload: pageNo
  }
}

export const clearBookData = () => {
  return {
    type: constants.ClEAR_BOOK_DATA
  }
}

export const getBooksList = pageNo => {
  return dispatch => {
    dispatch({ type: constants.FETCH_BOOKS_STARTED })
    bookService
      .getBooks(pageNo)
      .then(response => {
        if (response.status === responseCodes.OK) {
          dispatch({
            type: constants.FETCH_BOOKS_SUCCESS,
            payload: response.data
          })
        }
      })
      .catch(error => {
        dispatch({
          type: constants.FETCH_BOOK_FAILURE,
          payload: error
        })
      })
  }
}

export const getBookDetail = bookId => {
  return dispatch => {
    dispatch({ type: constants.FETCH_BOOK_STARTED })
    bookService
      .getBook(bookId)
      .then(response => {
        if (response.status === responseCodes.OK) {
          dispatch({
            type: constants.FETCH_BOOK_SUCCESS,
            payload: response.data
          })
        }
      })
      .catch(error => {
        dispatch({
          type: constants.FETCH_BOOK_FAILURE,
          payload: error
        })
        if (error.response.status === responseCodes.NOT_FOUND)
          history.replace(urls.notFound)
      })
  }
}

export const createBook = bookData => {
  return dispatch => {
    dispatch({ type: constants.CREATE_BOOK_STARTED })
    return bookService
      .newBook(bookData)
      .then(response => {
        if (response.status === responseCodes.CREATED) {
          dispatch({
            type: constants.CREATE_BOOK_SUCCESS,
            payload: response.data
          })
          history.push(`${urls.book}${response.data.id}`)
        }
      })
      .catch(error => {
        dispatch({
          type: constants.CREATE_BOOK_FAILURE,
          payload: error
        })
      })
  }
}

export const updateBookDetails = (bookId, bookData) => {
  return dispatch => {
    dispatch({ type: constants.UPDATE_BOOK_STARTED })
    return bookService
      .updateBook(bookId, bookData)
      .then(response => {
        if (response.status === responseCodes.OK) {
          dispatch({
            type: constants.UPDATE_BOOK_SUCCESS,
            payload: response.data
          })
          history.push(`${urls.book}${bookId}`)
        }
      })
      .catch(error => {
        dispatch({
          type: constants.UPDATE_BOOK_FAILURE,
          payload: error
        })
      })
  }
}

export const deleteBook = bookId => {
  return dispatch => {
    dispatch({ type: constants.DELETE_BOOK_STARTED })
    bookService
      .oremoveBook(bookId)
      .then(response => {
        if (response.status === responseCodes.NO_CONTENT) {
          dispatch({
            type: constants.DELETE_BOOK_SUCCESS,
            payload: bookId
          })
          history.push(urls.books)
        }
      })
      .catch(error => {
        dispatch({
          type: constants.DELETE_BOOK_FAILURE,
          payload: error
        })
        if (error.response.status === responseCodes.NOT_FOUND)
          history.replace(urls.notFound)
      })
  }
}
