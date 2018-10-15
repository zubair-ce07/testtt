import YTSearch from 'youtube-api-search';
import {YoutubeAPIKey} from '../configs/'

export const search = (term, callback) =>
  YTSearch({
    key: YoutubeAPIKey,
    term,
  }, callback);
