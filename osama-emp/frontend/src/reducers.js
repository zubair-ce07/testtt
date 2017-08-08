import { GET_PROFILE_END, REPLACE_DIRECTS_END } from "./actions";
import djangoapi from "./djangoapi";
import utils from "./utils";

const initialState = {
  profile: {},
  hierarchy: {
    username: "yasser",
    profile: "http://localhost:8000/employees/yasser/",
    first_name: "Yasser",
    last_name: "Bashir",
    gender: "M",
    date_of_birth: "2012-12-30",
    date_of_joining: "2016-10-26",
    job_title: "CEO",
    nationality: "",
    reports_to: null,
    directs: "osama"
  }
};

function rootReducer(state = initialState, action) {
  switch (action.type) {
    case GET_PROFILE_END:
      return Object.assign({}, state, {
        profile: action.profile
      });
    case REPLACE_DIRECTS_END:
      return Object.assign({}, state, {
        hierarchy: action.hierarchy
      });
    default:
      return state;
  }
}

export default rootReducer;
