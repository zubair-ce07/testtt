import { combineReducers } from 'redux';
import { reducer as formReducer } from 'redux-form';
import { reducer as toastrReducer} from 'react-redux-toastr'

import loginReducer from './login-reducer';
import profileReducer from './profile-reducer';
import searchReducer from './search_users-reducer';
import selectedUserReducer from './selected_user-reducer';
import traineesAssignedReducer from './trainees_assigned-reducer';
import trainerAssignedReducer from './trainer_assigned-reducer';
import assignmentsAssignedReducer from './assignments_assigned-reducer';
import assignmentReducer from './assignment-reducer';
import technologiesUsedReducer from './technologies_used-reducer';
import technologyReducer from './technology-reducer';
import { USER_LOGOUT } from '../config';

const appReducer = combineReducers({
    user: loginReducer,
    profile: profileReducer,
    search: searchReducer,
    selectedUser: selectedUserReducer,
    traineesAssigned: traineesAssignedReducer,
    trainerAssigned: trainerAssignedReducer,
    assignmentsAssigned: assignmentsAssignedReducer,
    assignmentDetails: assignmentReducer,
    technologiesUsed: technologiesUsedReducer,
    technologyDetails: technologyReducer,
    toastr: toastrReducer,
    form: formReducer
});

const rootReducer = (state, action) => {
    switch (action.type)
    {
        case USER_LOGOUT:
            state = undefined;
    }

    return appReducer(state, action)
};

export default rootReducer;
