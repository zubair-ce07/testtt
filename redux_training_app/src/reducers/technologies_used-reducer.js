import { TECHNOLOGIES_USED } from '../config'

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
        case TECHNOLOGIES_USED:
            return {
                loggedInUser: state.loggedInUser,
                searchedUsers: null,
                selectedUser: state.selectedUser,
                traineesAssigned: null,
                trainerAssigned: null,
                assignmentsAssigned: null,
                selectedAssignment: null,
                technologiesUsed: action.payload.data,
                selectedTechnology: null
            };
        default:
            return state;
    }
}