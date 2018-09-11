import axios from 'axios';

const ROOT_URL = 'http://127.0.0.1:8000/teams/';
export const FETCH_TEAMS = 'FETCH_TEAMS';

export function fetchTeams(term) {
  const url = ROOT_URL;
  const request = axios.get(url); // asynchronus request, returns a ReduxPromise

  return {
    type: FETCH_TEAMS,
    payload: request
  };
}

// axios({
//     method:'get',
//     url:'http://127.0.0.1:8000/teams/',
//     json: true,
//     })
// .then(function(response) {
//   console.log(response.data.results);
//   // this.setState({teams: response.data.results});
// });
