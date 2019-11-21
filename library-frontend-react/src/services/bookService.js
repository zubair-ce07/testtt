import baseService from "./baseService.js"

// export const getBook = bookId => {
//   return baseService.get(`/books/${bookyId}`)
// }

export const getBooks = searchQuery => {
  return baseService.get(`/books/`, {
    params: {
      search: searchQuery
    }
  })
}

// export const updateBook = (organizationId, bookyId, status) => {
//   return baseService.patch(`/book/${bookyId}`, {
//     status: status
//   })
// }
