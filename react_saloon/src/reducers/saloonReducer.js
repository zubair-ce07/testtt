import { FETCH_SALOON_SUCCESSFUL,FETCH_SALOON_FAILED,GET_SLOTS_SUCCESSFUL,
    GET_SLOTS_FAILED,GET_SLOTS_FOR_USER_SUCCESSFUL,GET_SLOTS_FOR_USER_FAILED,GET_RESERVATION_FOR_USER_SUCCESSFUL,GET_RESERVATION_FOR_USER_FAILED,
    GET_SALOON_RESERVATION_SUCCESSFUL,GET_SALOON_RESERVATION_FAILED,SLOTS_RESERVED_SUCCESSFUL,
    SLOTS_RESERVED_FAILED,DELETE_RESERVATION_SUCCESSFUL,DELETE_RESERVATION_FAILED,ADD_SLOTS_SUCESSFUL,
    ADD_SLOTS_FAILED} from '../constants/actionsTypeConstants';

const initState = {
    saloons: [],
    successStatus:true,
    reservations:[],
    time_slots:[],
    addTimeSlotSuccessStatus:true
};
const saloonReducer = (state = initState, action) => {
    switch (action.type) {
    case FETCH_SALOON_SUCCESSFUL:
        return {
            ...state,
            saloons: action.payload,
            successStatus: true
        };

    case FETCH_SALOON_FAILED:
        return {
            ...state,
            successStatus: false
        };
    case GET_SLOTS_SUCCESSFUL:
        return {
            ...state,
            time_slots: action.payload
        };
    case GET_SLOTS_FAILED:
        return {
            ...state,
            successStatus: false
        };
    case GET_SLOTS_FOR_USER_SUCCESSFUL:
        return {
            ...state,
            time_slots: action.payload
        };
    case GET_SLOTS_FOR_USER_FAILED:
        return {
            ...state,
            successStatus: false
        };
    case GET_RESERVATION_FOR_USER_SUCCESSFUL:
        return {
            ...state,
            reservations: action.payload
        };
    case GET_RESERVATION_FOR_USER_FAILED:
        return {
            ...state,
            successStatus: false
        };
    case GET_SALOON_RESERVATION_SUCCESSFUL:
        return {
            ...state,
            reservations: action.payload
        };
    case GET_SALOON_RESERVATION_FAILED:
        return {
            ...state,
            successStatus: false
        };
    case DELETE_RESERVATION_SUCCESSFUL:{
        let newReservations = [...state.reservations];
        newReservations = newReservations.filter((reservation) => reservation.id !== action.id);
        return {
            ...state,
            successStatus: false,
            reservations: newReservations
        };
    }
    case DELETE_RESERVATION_FAILED:
        return {
            ...state,
            successStatus: false
        };
    case SLOTS_RESERVED_SUCCESSFUL:{
        let newTimeSlots = [...state.time_slots];
        newTimeSlots.forEach(element => {
            if (action.time_slot === element.id) {
                element.reservation = true;
            }
        });

        return {
            ...state,
            time_slots: newTimeSlots,
            successStatus: true
        };
    }
    case SLOTS_RESERVED_FAILED:
        return {
            ...state,
            successStatus: false
        };
    case ADD_SLOTS_SUCESSFUL:
        return {
            ...state,
            addTimeSlotSuccessStatus: false
        };
    case ADD_SLOTS_FAILED:
        return {
            ...state,
            addTimeSlotSuccessStatus: false
        };

    default:
        return state;
    }

};
export default saloonReducer;