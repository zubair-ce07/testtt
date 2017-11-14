import { SEARCH_USERS } from '../config'

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
        case SEARCH_USERS:
            return {
                loggedInUser: state.loggedInUser,
                searchedUsers: action.payload.data,
                selectedUser: null,
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