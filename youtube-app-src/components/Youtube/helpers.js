import * as constants from '../../shared/constants';

export const urlFormer = (query, relatedVideoId) => {
  let url = `${constants.BASE_URL}?part=snippet&order=rating&`;
  url += `key=${constants.KEY}&type=video&`;
  if (query) {
    url += `q=${query}`;
  }
  if (relatedVideoId) {
    url += `relatedToVideoId=${relatedVideoId}`;
  }
  return url;
};

export const formSourcesList = data => {
  let listSources = [];
  for (let item of data.items) {
    let videoIcon = {
      title: item.snippet.title,
      description: item.snippet.description,
      thumbnail: item.snippet.thumbnails.default.url,
      id: item.id.videoId
    };
    listSources.push(videoIcon);
  }
  return listSources;
};
