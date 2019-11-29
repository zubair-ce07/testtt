import auth from "./authReducer"
import authors from "./authorsReducer"
import books from "./booksReducer"
import categories from "./categoriesReducer"
import { combineReducers } from "redux"
import publishers from "./publishersReducer"

const rootReducer = combineReducers({
  auth,
  authors,
  books,
  categories,
  publishers
})

export default rootReducer
