import { types } from "./types";

const updateForm = form => ({
  type: types.UPDATE_FORM,
  payload: {
    form
  }
});

export { updateForm };
