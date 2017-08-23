import axios from 'axios';
import { TRAINING_BASE_URL, TRAINER_ASSIGNED } from "../config"


export function trainerAssigned(trainee_id)
{
    const request = axios({
        method:'get',
        url: `${TRAINING_BASE_URL}trainees/${trainee_id}/trainer`,
        headers: {'Authorization': `Token ${localStorage.getItem('token')}`}
    });

    return {
        type: TRAINER_ASSIGNED,
        payload: request
    };
}