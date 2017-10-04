import { saveState } from '../localStorage'
import { LOGIN, LOGOUT} from '../actions/actions'

const defaultState = {
  isLoggedIn: false,
  username: '',
  token: '',
  id: ''
};
 
export default function authReducer(state = defaultState, action) {
  switch (action.type) {
    case LOGIN:
      const {username, token, id} = action
      const auth_state = {isLoggedIn: true, username: username, token: token, id: id}
      saveState(auth_state)
      return{ 
        isLoggedIn: true,
        username: username,
        token: token,
        id: id
      });
    case LOGOUT:
      saveState(defaultState)
      return { 
        isLoggedIn: false,
        username: '',
        token: '',
        id: ''
      });
    default:
      return state;
  }
}