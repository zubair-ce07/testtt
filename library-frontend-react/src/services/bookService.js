import { doDelete, doGet, doPost, doPut } from "services/baseService.js"

import responseCodes from "constants/responseCodes"

const bookService = {
  getBook: bookId => {
    return doGet(`/book/${bookId}`)
  },
  getBooks: (pageNo, searchQuery = null) => {
    return doGet(`/books/`, {
      params: {
        page: pageNo,
        search: searchQuery
      }
    })
  },
  newBook: data => {
    return doPost("/book/", data, responseCodes.CREATED)
  },
  updateBook: (bookId, data) => {
    return doPut(`/book/${bookId}/update`, data)
  },
  removeBook: bookId => {
    return doDelete(`/book/${bookId}/delete`)
  }
}

export default bookService
