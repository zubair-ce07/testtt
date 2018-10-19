import Service from '../users/service';
import history from '../../history';

import { failed, reset, loading, loaded, loadSignedInUser } from '../users/create/actions';

const service = new Service();

export const signOut = () => async dispatch => {
  dispatch(reset);
  dispatch(loading);
  const response = await service.signOut();
  dispatch(loaded);
  if (response.success) {
    dispatch(reset());
    history.push('/blogs');
  } else {
    dispatch(failed(response.data));
  }
};

export { loadSignedInUser };
