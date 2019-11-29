import baseService from "./baseService.js"
import urls from "../urls"

const authorService = {
  getAuthor: authorId => {
    return baseService.get(`/author/${authorId}`)
  },
  getAuthors: (pageNo, searchQuery = null) => {
    return baseService.get(`/authors/`, {
      params: {
        page: pageNo,
        search: searchQuery
      }
    })
  },
  getAuthorsData: () => {
    return baseService.get(urls.authorsData)
  }
}

export default authorService
