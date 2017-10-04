
function weatherApp(state = [], action) {
    if (action.type === 'SEARCH_BY_CITY'){
        return [
            action.data,
            ...state
        ]
    }
    return state
}

export default weatherApp;