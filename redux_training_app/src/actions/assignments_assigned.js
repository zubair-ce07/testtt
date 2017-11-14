import axios from 'axios';
import { TRAINING_BASE_URL, ASSIGNMENTS_ASSIGNED } from "../config"


export default function assignmentsAssigned(trainee_id)
{
    const request = axios({
        method:'get',
        url: `${TRAINING_BASE_URL}trainees/${trainee_id}/assignments`,
        headers: {'Authorization': `Token ${localStorage.getItem('token')}`}
    });

    return {
        type: ASSIGNMENTS_ASSIGNED,
        payload: request
    };
}