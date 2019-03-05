import {
  LOADING_USER, UPDATE_USER, RESET_USER, USER_ERRORS, USER_LOADED
} from './actions';

const INITIAL_STATE = {
  loading: false,
  loaded: false,
  user: {
    id: 0,
    first_name: '',
    last_name: '',
    username: '',
    password: '',
    confirm_password: '',
    email: '',
    phone_number: '',
  },
  errors: {},
};

const initializeState = () => {
  let state = INITIAL_STATE;
  let user = localStorage.getItem('user');
  if (user) {
    user = JSON.parse(user);
    state = { ...state, user: { ...state.user, ...user } };
  }

  return state;
};

export const UserReducer = (state = initializeState(), action) => {
  switch (action.type) {
    case LOADING_USER:
      return { ...state, loading: true };

    case USER_LOADED:
      return { ...state, loading: false, loaded: true };

    case RESET_USER:
      return INITIAL_STATE;

    case UPDATE_USER:
      return {
        ...state,
        user: { ...state.user, ...action.payload }
      };

    case USER_ERRORS:
      return { ...state, errors: action.payload };

    default:
      return state;
  }
};
