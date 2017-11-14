import { USER_PROFILE } from '../config'

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
        case USER_PROFILE:
            return {
                loggedInUser: action.payload,
                searchedUsers: null,
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