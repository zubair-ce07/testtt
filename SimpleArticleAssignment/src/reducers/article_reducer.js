import { FETCH_ARTICLES_LIST } from "../actions/index";

export default function (state=[], action) {

    switch (action.type) {
        case FETCH_ARTICLES_LIST:
            return action.payload.data;
    }
    return state;
}
