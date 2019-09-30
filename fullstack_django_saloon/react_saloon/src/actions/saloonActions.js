import { REACT_APP_API_ENDPOINT_BASE_URL } from '../constants/config';
import { apiEndPoints } from '../constants/apiEndPoints';
import { actionTypes} from '../constants/actionsTypeConstants';
import { reactAppConstants } from '../constants/constants';
import { getTokenHeader,makeApiUrl,makeGetCall,makeGetCallWithHeader,makeDeleteCallWithHeader,makePostCallWithHeader } from '../actions/utils';

export const fetchSaloons = () =>  
    dispatch => {
        makeGetCall(makeApiUrl(REACT_APP_API_ENDPOINT_BASE_URL,apiEndPoints.SHOP_API_SALOONS)).then((response) => {
            dispatch({ type: actionTypes.FETCH_SALOON_SUCCESSFUL, payload: response.data });
        }).catch(() => {
            dispatch({ type: actionTypes.FETCH_SALOON_FAILED });
        });

    };

export const saloonProfile = () =>
    dispatch =>
        makeGetCallWithHeader(makeApiUrl(REACT_APP_API_ENDPOINT_BASE_URL,apiEndPoints.SHOP_API_PROFILE), { headers: { [reactAppConstants.AUTHORIZATION]: getTokenHeader() } }).then((response) => {
            dispatch({ type: actionTypes.SALOON_PROFILE_SUCCESSFUL, payload: response.data });
        }).catch(() => {
            dispatch({ type: actionTypes.SALOON_PROFILE_FAILED });
        });

export const addTimeSlots = (data) =>
    dispatch =>
        makePostCallWithHeader(makeApiUrl(REACT_APP_API_ENDPOINT_BASE_URL,apiEndPoints.SHOP_API_MYSALOON), data, { headers: { [reactAppConstants.AUTHORIZATION]: getTokenHeader() } }).then((response) => {
            dispatch({ type: actionTypes.ADD_SLOTS_SUCCESSFUL });
            return response;
        }).catch((err) => {
            dispatch({ type: actionTypes.ADD_SLOTS_FAILED });
            return err;
        });

export const getTimeSlots = () =>
    dispatch => 
        makeGetCallWithHeader(makeApiUrl(REACT_APP_API_ENDPOINT_BASE_URL,apiEndPoints.SHOP_API_MYSALOON), { headers: { [reactAppConstants.AUTHORIZATION]: getTokenHeader() } }).then((response) => {
            dispatch({ type: actionTypes.GET_SLOTS_SUCCESSFUL, payload: response.data });
        }).catch(() => {
            dispatch({ type: actionTypes.GET_SLOTS_FAILED });
        });

export const getTimeSlotsForUser = shop_name =>
    dispatch =>
        makeGetCallWithHeader(makeApiUrl(REACT_APP_API_ENDPOINT_BASE_URL,apiEndPoints.SHOP_API_SHOP) + shop_name, { headers: { [reactAppConstants.AUTHORIZATION]: getTokenHeader() } }).then((response) => {
            dispatch({ type: actionTypes.GET_SLOTS_FOR_USER_SUCCESSFUL, payload: response.data });
        }).catch(() => {
            dispatch({ type: actionTypes.GET_SLOTS_FOR_USER_FAILED });
        });

export const getReservationsForUser = () =>
    dispatch =>
        makeGetCallWithHeader(makeApiUrl(REACT_APP_API_ENDPOINT_BASE_URL,apiEndPoints.CUSTOMER_API_MYRESERVATIONS), { headers: { [reactAppConstants.AUTHORIZATION]: getTokenHeader() } }).then((response) => {
            dispatch({ type: actionTypes.GET_RESERVATION_FOR_USER_SUCCESSFUL, payload: response.data });
        }).catch(() => {
            dispatch({ type: actionTypes.GET_RESERVATION_FOR_USER_FAILED });
        });

export const getSaloonReservations = () => 
    dispatch =>
        makeGetCallWithHeader(makeApiUrl(REACT_APP_API_ENDPOINT_BASE_URL,apiEndPoints.SHOP_API_MYRESERVATIONS), { headers: { [reactAppConstants.AUTHORIZATION]: getTokenHeader() } }).then((response) => {
            dispatch({ type: actionTypes.GET_SALOON_RESERVATION_SUCCESSFUL, payload: response.data });
        }).catch(() => {
            dispatch({ type: actionTypes.GET_SALOON_RESERVATION_FAILED });
        });

export const reserveSlotForUser = time_slot =>
    dispatch =>
        makePostCallWithHeader(makeApiUrl(REACT_APP_API_ENDPOINT_BASE_URL,apiEndPoints.SHOP_API_RESERVE_SLOT), { time_slot }, { headers: { [reactAppConstants.AUTHORIZATION]: getTokenHeader() } }).then(() => {
            dispatch({ type: actionTypes.SLOTS_RESERVED_SUCCESSFUL, time_slot });
        }).catch(() => {
            dispatch({ type: actionTypes.SLOTS_RESERVED_FAILED });
        });

export const cancelReservation = id =>
    dispatch =>
        makeDeleteCallWithHeader(makeApiUrl(REACT_APP_API_ENDPOINT_BASE_URL,apiEndPoints.SHOP_API_CANCEL_RESERVATION) + id, { headers: { [reactAppConstants.AUTHORIZATION]: getTokenHeader() } }).then(() => {
            dispatch({ type: actionTypes.DELETE_RESERVATION_SUCCESSFUL, id });
        }).catch(() => {
            dispatch({ type: actionTypes.DELETE_RESERVATION_FAILED });
        });

export const updateSaloonProfile = data => {
    const requestData = {
        'user': {
            'first_name': data.first_name,
            'last_name': data.last_name,
            'email': data.email,
            'username': data.username
        },
        'phone_no': data.phone_no,
        'address': data.address,
        'shop_name':data.shop_name
    };
    return dispatch =>
        makePostCallWithHeader(makeApiUrl(REACT_APP_API_ENDPOINT_BASE_URL,apiEndPoints.SHOP_API_PROFILE), requestData, { headers: { [reactAppConstants.AUTHORIZATION]: getTokenHeader() } }).then((response) => {
            dispatch({ type: actionTypes.SALOON_UPDATE_PROFILE_SUCCESSFUL, payload: response.data });
        }).catch(() => {
            dispatch({ type: actionTypes.SALOON_UPDATE_PROFILE_FAILED });
        });
};