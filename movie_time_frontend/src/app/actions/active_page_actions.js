import {SET_ACTIVE_PAGE} from './action_types'

export function setActivePage(active_page) {
    return {
        type: SET_ACTIVE_PAGE,
        payload: active_page
    };
}
