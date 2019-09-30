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

const formReducer = (state=initailState, action) => {
    switch(action.type) {
        case types.LOGIN_FORM:
            return({
                ...state,
                isLoginForm: !state.isLoginForm
            });
        default:
            return state;
    }

}

export default formReducer;
