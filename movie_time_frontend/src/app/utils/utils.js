import _ from 'lodash';

import {ROOT_URL} from "../actions/action_types";


export const getImageUrl = (path, size) => {
    return path ? `http://image.tmdb.org/t/p/${size}${path}` : '/images/no-img.png';
};

export const getUserPhoto = (path) => {
    return path !== null ? path : '/images/avatar.jpg';
};

export const cutString = (string, no_of_characters, hard=false) => {
    try {
        if (hard && string.length > no_of_characters)
            return string.substring(0, no_of_characters-3) + '...';
        else if(hard && string.length <= no_of_characters)
            return string;

        let cut = string.indexOf(' ', no_of_characters);
        if (cut === -1) return string;
        return string.substring(0, cut) + '...'
    }
    catch (TypeError){
        return 'Not Available';
    }
};

export const updateUserStatusesForMovie = (state, action, remove=false) => {
    const newState = [];
    _.map(state, movie => {
        newState.push(movie);
        if(movie.id === action.payload.data.movie) {
            movie.user_statuses = action.payload.data;
            if (remove) newState.pop()
        }
    });
    return newState;
};

export const updateUserStatusesInActivities = (state, action) => {
    const newState = [];
    _.map(state, activity => {
        if (activity.movie.id === action.payload.data.movie) activity.movie.user_statuses = action.payload.data;
        newState.push(activity);
    });
    return newState;
};

export const nFormatter = (num, digits) => {
  const si = [
    { value: 1E9,  symbol: "B" },
    { value: 1E6,  symbol: "M" },
    { value: 1E3,  symbol: "k" }
  ], rx = /\.0+$|(\.[0-9]*[1-9])0+$/;

  for (let i = 0; i < si.length; i++) {
    if (num >= si[i].value) {
      return (num / si[i].value).toFixed(digits).replace(rx, "$1") + si[i].symbol;
    }
  }

  return num.toFixed(digits).replace(rx, "$1");
};
