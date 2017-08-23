import { ASSIGNMENTS_ASSIGNED } from '../config'

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
        case ASSIGNMENTS_ASSIGNED:
            return {
                loggedInUser: state.loggedInUser,
                searchedUsers: null,
                selectedUser: state.selectedUser,
                traineesAssigned: null,
                trainerAssigned: null,
                assignmentsAssigned: action.payload.data,
                selectedAssignment: null,
                technologiesUsed: null,
                selectedTechnology: null
            };
        default:
            return state;
    }
}