import auth from "reducers/authReducer"
import authors from "reducers/authorsReducer"
import books from "reducers/booksReducer"
import categories from "reducers/categoriesReducer"
import { combineReducers } from "redux"
import publishers from "reducers/publishersReducer"

const rootReducer = combineReducers({
  auth,
  authors,
  books,
  categories,
  publishers
})

export default rootReducer
