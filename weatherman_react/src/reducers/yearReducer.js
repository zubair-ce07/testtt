export default function (state=[], action) {
    switch (action.type) {
        case 'FETCH_YEAR_SUCCEEDED':
            state = action.payload;
            break;
        case 'FETCH_YEAR_EMPTY':
            state = [];
            break;
        case 'FETCH_YEARS_FAILED':
            state = [];
            break;
        default:
            return state;
    }
    return state;
}