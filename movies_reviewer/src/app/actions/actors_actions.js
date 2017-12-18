import TheMovieDatabase from 'themoviedatabase';

export const FETCH_ACTOR = 'FETCH_ACTOR';

const MDB = new TheMovieDatabase('7b43db1b983b055bffd7534a06cafd6c');

export function fetchActor(id) {
    const request = MDB.people.details(null, {person_id: id});

    return {
        type: FETCH_ACTOR,
        payload: request
    };
}
