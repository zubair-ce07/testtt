import authReducer from './authReducer';
import { combineReducers } from 'redux';

import productReducer from './productReducer';
import modalReducer from './modalReducer';


const rootReducer = combineReducers({
    auth: authReducer,
    product: productReducer,
    modal: modalReducer
})

export default rootReducer;
