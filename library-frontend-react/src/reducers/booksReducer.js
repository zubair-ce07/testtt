import { formatDate, getPageNumberFromUrl } from "../util/utils"

import { PAGE_SIZE } from "../contants/global"
import constants from "../contants/action_types/book_constants"

const initialState = {
  loading: false,
  books: [],
  book: {
    title: "",
    isbn: "",
    pages: 1,
    date_published: formatDate(new Date(), "YYYY-MM-DD"),
    authors: [],
    publisher: {},
    categories: []
  },
  error: null,

  next: null,
  previous: null,
  pagesCount: 1,
  totalCount: 0,
  currentPageNumber: 1
}

const booksReducer = (state = initialState, action) => {
  switch (action.type) {
    case constants.FETCH_BOOKS_STARTED:
    case constants.FETCH_BOOK_STARTED:
    case constants.CREATE_BOOK_STARTED:
    case constants.DELETE_BOOK_STARTED:
      return {
        ...state,
        loading: true
      }

    case constants.ClEAR_BOOK_DATA:
      return {
        ...state,
        book: initialState.book
      }

    case constants.SET_CURRENT_PAGE:
      return {
        ...state,
        currentPageNumber: action.payload
      }

    case constants.FETCH_BOOKS_SUCCESS:
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

        books: results
      }
    case constants.FETCH_BOOK_SUCCESS:
      return {
        ...state,
        loading: false,
        error: null,
        book: action.payload
      }
    case constants.DELETE_BOOK_SUCCESS:
      return {
        ...state,
        loading: false,
        error: null,
        books: [...state.books.filter(book => book.id === action.payload)],
        book: {}
      }
    case constants.UPDATE_BOOK_SUCCESS:
    case constants.CREATE_BOOK_SUCCESS:
      return {
        ...state,
        loading: false,
        error: null,
        book: [...state.books, action.payload]
      }

    case constants.FETCH_BOOKS_FAILURE:
    case constants.FETCH_BOOK_FAILURE:
    case constants.CREATE_BOOK_FAILURE:
      return {
        ...state,
        loading: false,
        error: action.payload
      }
    default:
      return state
  }
}

export default booksReducer
