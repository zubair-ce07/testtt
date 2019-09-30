import { actionTypes } from '../constants/actionsTypeConstants';

const initState = {
    saloons: [],
    successStatus:true,
    reservations:[],
    timeSlots:[],
    addTimeSlotSuccessStatus:true
};
const saloonReducer = (state = initState, action) => {
    switch (action.type) {
    case actionTypes.FETCH_SALOON_SUCCESSFUL:
        return {
            ...state,
            saloons: action.payload,
            successStatus: true
        };
    case actionTypes.FETCH_SALOON_FAILED:
        return {
            ...state,
            successStatus: false
        };
    case actionTypes.GET_SLOTS_SUCCESSFUL:
        return {
            ...state,
            timeSlots: action.payload
        };
    case actionTypes.GET_SLOTS_FAILED:
        return {
            ...state,
            successStatus: false
        };
    case actionTypes.GET_SLOTS_FOR_USER_SUCCESSFUL:
        return {
            ...state,
            timeSlots: action.payload
        };
    case actionTypes.GET_SLOTS_FOR_USER_FAILED:
        return {
            ...state,
            successStatus: false
        };
    case actionTypes.GET_RESERVATION_FOR_USER_SUCCESSFUL:
        return {
            ...state,
            reservations: action.payload
        };
    case actionTypes.GET_RESERVATION_FOR_USER_FAILED:
        return {
            ...state,
            successStatus: false
        };
    case actionTypes.GET_SALOON_RESERVATION_SUCCESSFUL:
        return {
            ...state,
            reservations: action.payload
        };
    case actionTypes.GET_SALOON_RESERVATION_FAILED:
        return {
            ...state,
            successStatus: false
        };
    case actionTypes.DELETE_RESERVATION_SUCCESSFUL:{
        let newReservations = [...state.reservations];
        newReservations = newReservations.filter((reservation) => reservation.id !== action.id);
        return {
            ...state,
            successStatus: false,
            reservations: newReservations
        };
    }
    case actionTypes.DELETE_RESERVATION_FAILED:
        return {
            ...state,
            successStatus: false
        };
    case actionTypes.SLOTS_RESERVED_SUCCESSFUL:{
        let newTimeSlots = [...state.timeSlots];
        newTimeSlots.forEach(element => {
            if (action.time_slot === element.id) {
                element.reservation = true;
            }
        });
        return {
            ...state,
            timeSlots: newTimeSlots,
            successStatus: true
        };
    }
    case actionTypes.SLOTS_RESERVED_FAILED:
        return {
            ...state,
            successStatus: false
        };
    case actionTypes.ADD_SLOTS_SUCCESSFUL:
        return {
            ...state,
            addTimeSlotSuccessStatus: true
        };
    case actionTypes.ADD_SLOTS_FAILED:
        return {
            ...state,
            addTimeSlotSuccessStatus: false
        };
    default:
        return state;
    }
};
export default saloonReducer;