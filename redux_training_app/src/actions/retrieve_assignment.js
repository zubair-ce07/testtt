import axios from 'axios';
import { TRAINING_BASE_URL, ASSIGNMENT_DETAILS } from "../config"


export function retrieveAssignmentDetails(assignment_id)
{
    const request = axios({
        method:'get',
        url: `${TRAINING_BASE_URL}assignments/${assignment_id}`,
        headers: {'Authorization': `Token ${localStorage.getItem('token')}`}
    });

    return {
        type: ASSIGNMENT_DETAILS,
        payload: request
    };
}