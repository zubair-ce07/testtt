import YTSearch from 'youtube-api-search'

const API_KEY = 'AIzaSyB5wN5GvFkR7FSuiOaD5LC0svpx8WYlX4A';

export const search = (searchTerm) => {
    return dispatch => getVideos(searchTerm, dispatch);
};

const getVideos = (searchTerm, dispatch) => {
    YTSearch({key: API_KEY, term: searchTerm}, (videos) => dispatch(searchVideos(videos))

    )
};

const searchVideos = function(data){
    return {
        type: 'SEARCH_VIDEOS',
        data: data
    }
};


export const showDetail = function (video) {
    return {
        type: 'SHOW_DETAIL',
        data: video
    }

};
