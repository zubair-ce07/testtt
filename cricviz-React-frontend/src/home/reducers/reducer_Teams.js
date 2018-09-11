import { FETCH_TEAMS } from '../actions/FetchTeams';

export default function(state = [], action) {

  switch (action.type) {
  case FETCH_TEAMS:
    // return state.concat([action.payload.data]);   // as we have multiple cities incoming
    // dont use state.push as it will mutate the state, .concat returns a new state instance
    return [ action.payload.data, ...state ];
  }
  return state;
}
