import axios from 'axios';
import { TRAINING_BASE_URL, USER_PROFILE } from "../config"


export function updateImage(props) {
    let data = new FormData();
    data.append('picture', props.picture['0']);

    let config = {
        headers: {'Authorization': `Token ${localStorage.getItem('token')}`},
    };

    const request = axios.patch(`${TRAINING_BASE_URL}profile/`, data, config);

    return {
        type: USER_PROFILE,
        payload: request
    };
}