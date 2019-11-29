import baseService from "./baseService.js"

export const getBook = bookId => {
  return baseService.get(`/book/${bookId}`)
}

const bookService = {
  getBook: bookId => {
    return baseService.get(`/book/${bookId}`)
  },
  getBooks: (pageNo, searchQuery = null) => {
    return baseService.get(`/books/`, {
      params: {
        page: pageNo,
        search: searchQuery
      }
    })
  },
  newBook: data => {
    return baseService.post("/book/", data)
  },
  updateBook: (bookId, data) => {
    return baseService.put(`/book/${bookId}/update`, data)
  },
  removeBook: bookId => {
    return baseService.delete(`/book/${bookId}/delete`)
  }
}

export default bookService
