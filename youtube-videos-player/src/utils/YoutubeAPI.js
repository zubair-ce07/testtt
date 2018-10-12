import YTSearch from 'youtube-api-search';
import * as configs from '../configs/configurations'

export const search = (searchQuery, callback) =>
    YTSearch({
        key: configs.YoutubeAPIKey,
        term: searchQuery
    }, callback);
