import axios from 'axios';
import { TRAINING_BASE_URL, TRAINER_SIGNUP } from "../config"


export function signupTrainer(props) {
    let data = new FormData();
    data.append('username', props.username);
    data.append('first_name', props.first_name);
    data.append('last_name', props.last_name);
    data.append('password', props.password);
    data.append('picture', props.picture['0']);

    const request = axios.post(`${TRAINING_BASE_URL}trainer_signup/`, data);

    return {
        type: TRAINER_SIGNUP,
        payload: request
    };
}