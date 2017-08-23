import axios from 'axios';
import { TRAINING_BASE_URL, TRAINEE_SIGNUP } from "../config"


export function signupTrainee(props){

    let data = new FormData();
    data.append('username', props.username);
    data.append('first_name', props.first_name);
    data.append('last_name', props.last_name);
    data.append('password', props.password);
    data.append('picture', props.picture['0']);

    const request = axios.post(`${TRAINING_BASE_URL}trainee_signup/`, data);

    return {
        type: TRAINEE_SIGNUP,
        payload: request
    };
}