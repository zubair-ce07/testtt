import { doGet } from "services/baseService.js"
import urls from "urls"

const authorService = {
  getAuthor: authorId => {
    return doGet(`/author/${authorId}`)
  },
  getAuthors: (pageNo, searchQuery = null) => {
    return doGet(`/authors/`, {
      params: {
        page: pageNo,
        search: searchQuery
      }
    })
  },
  getAuthorsData: () => {
    return doGet(urls.authorsData)
  }
}

export default authorService
