import { combineReducers } from "redux"
import books from "./booksReducer"
import auth from "./authReducer"

const rootReducer = combineReducers({
  auth,
  books
})

export default rootReducer
