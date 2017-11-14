import axios from 'axios';
import { TRAINING_BASE_URL, USER_DETAILS } from "../config"


export function retrieveTrainerDetails(trainer_id)
{
    const request = axios({
        method:'get',
        url: `${TRAINING_BASE_URL}trainers/${trainer_id}`,
        headers: {'Authorization': `Token ${localStorage.getItem('token')}`}
    });

    return {
        type: USER_DETAILS,
        payload: request
    };
}