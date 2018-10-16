import YTSearch from 'youtube-api-search';
import { YOUTUBE_API_KEY as key } from '../configs/';

export const search = (term, callback) =>
  YTSearch({
    key,
    term
  }, callback);
