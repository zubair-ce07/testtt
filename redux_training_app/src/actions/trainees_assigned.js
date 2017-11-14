import axios from 'axios';
import { TRAINING_BASE_URL, TRAINEES_ASSIGNED } from "../config"


export function traineesAssigned(trainer_id)
{
    const request = axios({
        method:'get',
        url: `${TRAINING_BASE_URL}trainers/${trainer_id}/trainees`,
        headers: {'Authorization': `Token ${localStorage.getItem('token')}`}
    });

    return {
        type: TRAINEES_ASSIGNED,
        payload: request
    };
}