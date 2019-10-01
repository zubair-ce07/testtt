import { types } from "./types";

const updateUser = user => ({
  type: types.UPDATE_USER,
  payload: {
    user
  }
});

export { updateUser };
