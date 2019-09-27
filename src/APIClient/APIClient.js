import axios from "axios";
import {
    friendListEndpoint,
    groupJoinEndpoint,
    prependDomain,
    userProfileEndpoint
} from "../Utils/constants";

export const UserProfileAPI = () => {
    return axios.get(userProfileEndpoint)
};

export const GroupDataAPI = () => {
    return axios.get(groupJoinEndpoint)
};

export const WorkInformationAPI = link => {
    return axios.get(prependDomain(link))
};

export const AcademicInformationAPI = link => {
    return axios.get(prependDomain(link))
};

export const FriendListAPI = () => {
    return axios.get(friendListEndpoint)
};
