import authReducer from './authReducer';
import productReducer from './productReducer';
import modalReducer from './modalReducer';
import { combineReducers } from 'redux';

const rootReducer = combineReducers({
    auth: authReducer,
    product: productReducer,
    modal: modalReducer
})

export default rootReducer;
