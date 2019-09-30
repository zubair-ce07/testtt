import {types} from "../actions/types";

const initailState = {
    loading: false,
    user: {
      email: "",
      first_name: "",
      last_name: "",
      gender: "",
      date_of_birth:  "",
      password: "",
      confirm_password: ""
    },
    error: null,
    isLoginForm: true
  };

const userReducer = (state = initailState, action) => {
    switch(action.type) {
        case types.UPDATE_USER:
            return {
                ...state,
                user: action.payload.user
            }
        default:
            return state;
    }
}

export default userReducer;
