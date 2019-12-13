import { doGet } from "services/baseService.js"
import urls from "urls"

const publisherService = {
  getPublisher: publisherId => {
    return doGet(`/publisher/${publisherId}`)
  },

  getPublishers: (pageNo, searchQuery = null) => {
    return doGet(`/publishers/`, {
      params: {
        page: pageNo,
        search: searchQuery
      }
    })
  },

  getPublishersData: () => {
    return doGet(urls.publishersData)
  }
}

export default publisherService
