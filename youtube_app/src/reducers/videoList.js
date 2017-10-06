const videoList = (state = [], action) => {
    switch (action.type) {
        case 'SEARCH_VIDEOS':
            return action.data;
        default:
            return state
    }
};

export default videoList
