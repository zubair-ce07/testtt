import localStorage from 'local-storage';
import axios from 'axios';
import { reactAppConstants } from '../constants/constants';

export const getTokenHeader = ()=>
    'Token '.concat(localStorage.get(reactAppConstants.TOKEN));

export const makeApiUrl = (baseApiUrl,apiEndpoint)=>
    baseApiUrl+apiEndpoint;

export const makeGetCall = (url)=>
    axios.get(url);

export const makeGetCallWithHeader = (url,headers)=>
    axios.get(url,headers);

export const makePostCall = (url,requestData)=>
    axios.post(url,requestData);
    
export const makePostCallWithHeader = (url,requestData,headers)=>
    axios.post(url,requestData,headers);

export const makeDeleteCallWithHeader = (url,headers)=>
    axios.delete(url,headers);