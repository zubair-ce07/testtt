const selectedVideo = (state = '', action) => {
    switch (action.type) {
        case 'SHOW_DETAIL':
            return action.data;
        default:
            return state
    }
};

export default selectedVideo;
