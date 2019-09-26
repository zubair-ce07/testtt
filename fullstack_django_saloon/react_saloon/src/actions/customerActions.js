import { actionTypes } from '../constants/actionsTypeConstants';
import { REACT_APP_API_ENDPOINT_BASE_URL } from '../constants/config';
import { apiEndPoints } from '../constants/apiEndPoints';
import { reactAppConstants } from '../constants/constants';
import { getTokenHeader,makeApiUrl, makeGetCallWithHeader,makePostCallWithHeader } from './utils';

export const customerProfile = () => 
    dispatch =>
        makeGetCallWithHeader(makeApiUrl(REACT_APP_API_ENDPOINT_BASE_URL,apiEndPoints.CUSTOMER_API_PROFILE), { headers: { [reactAppConstants.AUTHORIZATION]: getTokenHeader() } }).then((response) => {
            dispatch({ type: actionTypes.CUSTOMER_PROFILE_SUCCESSFUL, payload: response.data });
        }).catch(() => {
            dispatch({ type: actionTypes.CUSTOMER_PROFILE_FAILED });
        });
        
export const updateCustomerProfile = data => {
    const requestData = {
        'user': {
            'first_name': data.first_name,
            'last_name': data.last_name,
            'email': data.email,
            'username': data.username
        },
        'phone_no': data.phone_no,
    };
    return dispatch => 
        makePostCallWithHeader(makeApiUrl(REACT_APP_API_ENDPOINT_BASE_URL,apiEndPoints.CUSTOMER_API_PROFILE), requestData, { headers: { [reactAppConstants.AUTHORIZATION]: getTokenHeader() } }).then((response) => {
            dispatch({ type: actionTypes.CUSTOMER_UPDATE_PROFILE_SUCCESSFUL, payload: response.data });
            return response;
        }).catch((err) => {
            dispatch({ type: actionTypes.CUSTOMER_UPDATE_PROFILE_FAILED });
            return err;
        });
};