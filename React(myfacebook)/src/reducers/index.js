import { combineReducers } from 'redux';
import { reducer as formReducer } from 'redux-form';
import newsListReducer from '../reducers/NewsListReducer';
import newsDetailReducer from '../reducers/NewsDetailReducer'
import loginReducer from '../reducers/LoginReducer'

const appReducer = combineReducers({
    loginReducer,
    newsListReducer,
    newsDetailReducer,
    form: formReducer
});

const rootReducer = (state, action) => {
    switch (action.type)
    {
        case 'USER_LOGOUT':
            state = undefined;
    }

    return appReducer(state, action)
};

export default rootReducer;
