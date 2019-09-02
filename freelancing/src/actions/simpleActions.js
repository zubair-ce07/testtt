import { SIMPLE_ACTION } from "./types";

export const simpleAction = () => dispatch => {
    dispatch({ type: SIMPLE_ACTION, payload: "TESTING A SIMPLE ACTION" })
}