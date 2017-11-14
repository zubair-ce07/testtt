import axios from 'axios';
import { TRAINING_BASE_URL, USER_DETAILS } from "../config"


export function retrieveTraineeDetails(trainee_id)
{
    const request = axios({
        method:'get',
        url: `${TRAINING_BASE_URL}trainees/${trainee_id}`,
        headers: {'Authorization': `Token ${localStorage.getItem('token')}`}
    });

    return {
        type: USER_DETAILS,
        payload: request
    };
}