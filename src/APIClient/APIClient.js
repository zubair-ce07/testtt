import axios from "axios";
import {
    friendlist_apiendpoint,
    groupjoin_apiendpoint,
    prepend_domain,
    userprofile_apiendpoint
} from "../Utils/constants";

export const UserProfileAPI = () => {
    return axios.get(userprofile_apiendpoint)
};

export const GroupDataAPI = () => {
    return axios.get(groupjoin_apiendpoint)
};

export const WorkInformationAPI = link => {
    return axios.get(prepend_domain(link))
};

export const AcademicInformationAPI = link => {
    return axios.get(prepend_domain(link))
};

export const FriendListAPI = () => {
    return axios.get(friendlist_apiendpoint)
};
