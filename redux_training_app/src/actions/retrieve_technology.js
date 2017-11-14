import axios from 'axios';
import { TRAINING_BASE_URL, TECHNOLOGY_DETAILS} from "../config"


export function retrieveTechnologyDetails(technology_id)
{
    const request = axios({
        method:'get',
        url: `${TRAINING_BASE_URL}technologies/${technology_id}`,
        headers: {'Authorization': `Token ${localStorage.getItem('token')}`}
    });

    return {
        type: TECHNOLOGY_DETAILS,
        payload: request
    };
}