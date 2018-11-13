import * as constants from './constants.js';

export const urlFormer = (query, relatedVideoId) => {
  let url = `${constants.BASE_URL}?part=snippet&order=rating&`
  url += `key=${constants.KEY}&type=video&`
  if(query) {
    url+=`q=${query}`
  }
  if(relatedVideoId) {
    url+=`relatedToVideoId=${relatedVideoId}`
  }
  return url
}


export const fetchData = (url) => {
  return fetch(url)
    .then(response => response.json())
    .catch(console.error);
}
