import { GET_PROFILE_END, REPLACE_DIRECTS } from "./actions";
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
    directs: [
      {
        username: "ayesha",
        profile: "http://localhost:8000/employees/ayesha/",
        first_name: "Ayesha",
        last_name: "Mahmood",
        gender: "F",
        date_of_birth: "2000-11-30",
        date_of_joining: "2009-12-04",
        job_title: "HR Manager",
        nationality: "Pakistani",
        reports_to: "http://localhost:8000/employees/yasser/",
        directs: null
      },
      {
        username: "abuzer",
        profile: "http://localhost:8000/employees/abuzer/",
        first_name: "Abu",
        last_name: "Zer",
        gender: "M",
        date_of_birth: "1981-01-31",
        date_of_joining: "2010-02-01",
        job_title: "DEO",
        nationality: "Lahore",
        reports_to: "http://localhost:8000/employees/yasser/",
        directs: null
      }
    ]
  }
};

function rootReducer(state = initialState, action) {
  switch (action.type) {
    case GET_PROFILE_END:
      return Object.assign({}, state, {
        profile: action.profile
      });
    case REPLACE_DIRECTS:
      let directs = djangoapi.getDirects(action.username, data => {
        console.log(data);
      });

      return Object.assign({}, state, {
        hierarchy: action.hierarchy
      });
    default:
      return state;
  }
}

export default rootReducer;
