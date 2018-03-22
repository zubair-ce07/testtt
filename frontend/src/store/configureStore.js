

import {createStore, applyMiddleware, combineReducers} from 'redux';
import rootReducer from '../reducers/index';
import { reducer as reduxFormReducer } from 'redux-form';

import thunk from 'redux-thunk';

export default function configureStore() {
    return createStore(
        combineReducers({
            rootReducer,
            form: reduxFormReducer
        }),
        applyMiddleware(thunk)
    )
}

