import { USER_DETAILS } from '../config'

const INITIAL_STATE = {
    loggedInUser: null,
    searchedUsers: null,
    selectedUser: null,
    traineesAssigned: [],
    trainerAssigned: null,
    assignmentsAssigned: null,
    selectedAssignment: null,
    technologiesUsed: null,
    selectedTechnology: null
};

export default function(state=INITIAL_STATE, action)
{
    switch (action.type){
        case USER_DETAILS:
            return {
                loggedInUser: state.loggedInUser,
                searchedUsers: null,
                selectedUser: action.payload.data,
                traineesAssigned: [],
                trainerAssigned: null,
                assignmentsAssigned: null,
                selectedAssignment: null,
                technologiesUsed: null,
                selectedTechnology: null
            };
        default:
            return state;
    }
}