import axios from 'axios';
import { TRAINING_BASE_URL, TECHNOLOGIES_USED } from "../config"


export default function assignmentsAssigned(assignment_id)
{
    const request = axios({
        method:'get',
        url: `${TRAINING_BASE_URL}assignments/${assignment_id}/technologies`,
        headers: {'Authorization': `Token ${localStorage.getItem('token')}`}
    });

    return {
        type: TECHNOLOGIES_USED,
        payload: request
    };
}