import baseService from "./baseService.js"
import urls from "../urls"

const publisherService = {
  getPublisher: publisherId => {
    return baseService.get(`/publisher/${publisherId}`)
  },

  getPublishers: (pageNo, searchQuery = null) => {
    return baseService.get(`/publishers/`, {
      params: {
        page: pageNo,
        search: searchQuery
      }
    })
  },

  getPublishersData: () => {
    return baseService.get(urls.publishersData)
  }
}

export default publisherService
