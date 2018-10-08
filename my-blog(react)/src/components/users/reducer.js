import { CLEAR_USER, UPDATE_USER } from '../../consts';

const INITIAL_STATE = {
  id: 0,
  first_name: '',
  last_name: '',
  username: '',
  password: '',
  confirm_password: '',
  email: '',
  errors: {},
};

const initiate_state = () => {
  let user = localStorage.getItem('user');
  let state = INITIAL_STATE;
  if (user) {
    user = JSON.parse(user);
    state = { ...state, ...user };
  }

  return state;
};

export default (state = initiate_state(), action) => {
  switch (action.type) {
    case UPDATE_USER:
      return { ...state, ...action.payload };
    case CLEAR_USER:
      return INITIAL_STATE;
    default:
      return state;
  }
};
