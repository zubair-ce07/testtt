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
        case 'GET_SALOON_RESERVATION_SUCESSFUL':
            return {
                ...state,
                reservations: action.payload
            }
        case 'GET_SALOON_RESERVATION_FAILED':
            return {
                ...state,
                successStatus: false
            }
        case 'DELETE_RESERVATION_SUCESSFUL':
            let newReservations = [...state.reservations]
            newReservations = newReservations.filter((reservation) => reservation.id !== action.id)
            return {
                ...state,
                successStatus: false,
                reservations: newReservations
            }
        case 'DELETE_RESERVATION_FAILED':
            return {
                ...state,
                successStatus: false
            }
        case 'SLOTS_RESERVED_SUCESSFUL':
            let newTimeSlots = [...state.time_slots]
            newTimeSlots.forEach(element => {
                if (action.time_slot === element.id) {
                    element.reservation = true
                }
            });

            return {
                ...state,
                time_slots: newTimeSlots,
                successStatus: true
            }
        case 'SLOTS_RESERVED_FAILED':
            return {
                ...state,
                successStatus: false
            }

        default:
            return state;
    }

}
export default saloonReducer;