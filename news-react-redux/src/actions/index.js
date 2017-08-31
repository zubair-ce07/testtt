//_______________________Application constants____________________________
const actions = {
    ADD_NEWS: "ADD_NEWS",
    SET_VISIBILITY_FILTER: "SET_VISIBILITY_FILTER",
    USER_LOGOUT: 'USER_LOGOUT',
    REFRESH_STATE: 'REFRESH_STATE',
    SET_DETAILED_NEWS_ID: 'SET_DETAILED_NEWS_ID',
    SET_SEARCH_TEXT: 'SET_SEARCH_TEXT',
    SET_USER: 'SET_USER',
};
const filters = {
    SHOW_ALL: "SHOW_ALL",
    SHOW_BY_SEARCH: "SHOW_BY_SEARCH",
    SHOW_BY_ID: "SHOW_BY_ID",
};

const refreshState = () => {
    return {
        type: actions.REFRESH_STATE,
    };
};

const setVisibilityFilter = (visibilityFilter) => {
    return {
        type: actions.SET_VISIBILITY_FILTER,
        visibilityFilter,
    };
};

const setSearchText = (searchText) => {
    return {
        type: actions.SET_SEARCH_TEXT,
        searchText,
    };
};

const setUser = (username, token) => {
    return {
        type: actions.SET_USER,
        username,
        token,
    }
};

const setDetailedNewsId = (id) =>{
    return{
        type:actions.SET_DETAILED_NEWS_ID,
        id,
    }
};
const addNews = (news) => {
    return {
        type: actions.ADD_NEWS,
        id: news.id,
        title: news.title,
        content: news.content,
        image_url: news.image_url,
        publisher: news.publisher,
        pub_date: news.pub_date,
    };
};

export {
    actions, filters, refreshState, addNews,
    setVisibilityFilter, setSearchText, setUser,
    setDetailedNewsId,
};