import authReducer from './authReducer';
import productReducer from './productReducer';
import modalReducer from './modalReducer';
import cartReducer from './cartReducer'
import { combineReducers } from 'redux';

const rootReducer = combineReducers({
    auth: authReducer,
    product: productReducer,
    modal: modalReducer,
    cart: cartReducer
})

export default rootReducer;
