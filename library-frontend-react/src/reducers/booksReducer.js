import {
  FETCH_BOOKS_STARTED,
  FETCH_BOOKS_SUCCESS,
  FETCH_BOOKS_FAILURE
} from "../contants/action_types/book_constants"

const initialState = {
  loading: false,
  books: [],
  error: null
}

const booksReducer = (state = initialState, action) => {
  switch (action.type) {
    case FETCH_BOOKS_STARTED:
      return {
        ...state,
        loading: true
      }
    case FETCH_BOOKS_SUCCESS:
      return {
        ...state,
        loading: false,
        error: null,
        books: [...state.books, action.payload.results]
      }
    case FETCH_BOOKS_FAILURE:
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
