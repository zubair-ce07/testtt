import { ASSIGNMENT_DETAILS } from '../config'

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
        case ASSIGNMENT_DETAILS:
            return {
                loggedInUser: state.loggedInUser,
                searchedUsers: null,
                selectedUser: state.selectedUser,
                traineesAssigned: null,
                trainerAssigned: null,
                assignmentsAssigned: null,
                selectedAssignment: action.payload.data,
                technologiesUsed: null,
                selectedTechnology: null
            };
        default:
            return state;
    }
}