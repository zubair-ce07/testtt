export default function (state=null, action) {
    switch (action.type) {
        case 'FETCH_CITIES_SUCCEEDED':
            state = action.payload;
            break;
        default:
            return state
    }
    return state;
    
}