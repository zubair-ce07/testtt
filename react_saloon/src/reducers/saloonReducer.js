const initState = {
    saloons: []
}
const saloonReducer = (state = initState, action) => {
    switch (action.type) {
        case 'FETCH_SALOON_SUCESSFUL':
            return {
                ...state,
                saloons: action.payload,
                successStatus: true
            }

        case 'FETCH_SALOON_FAILED':
            return {
                ...state,
                successStatus: false
            }
        case 'GET_SLOTS_SUCESSFUL':
            return {
                ...state,
                time_slots: action.payload
            }
        case 'GET_SLOTS_FAILED':
            return {
                ...state,
                successStatus: false
            }
        case 'GET_SLOTS_FOR_USER_SUCESSFUL':
            return {
                ...state,
                time_slots: action.payload
            }
        case 'GET_SLOTS_FOR_USER_FAILED':
            return {
                ...state,
                successStatus: false
            }
        case 'GET_RESERVATION_FOR_USER_SUCESSFUL':
            return {
                ...state,
                reservations: action.payload
            }
        case 'GET_RESERVATION_FOR_USER_FAILED':
            return {
                ...state,
                successStatus: false
            }

        default:
            return state;
    }

}
export default saloonReducer;