import TheMovieDatabase from 'themoviedatabase';

export const FETCH_MOVIES = 'FETCH_MOVIES';
export const FETCH_MOVIE = 'FETCH_MOVIE';


const MDB = new TheMovieDatabase('7b43db1b983b055bffd7534a06cafd6c');

export function fetchMovies(term) {
    const request = term === '' ? MDB.movies.nowPlaying() : MDB.search.movies({query: term});

    return {
        type: FETCH_MOVIES,
        payload: request
    };
}

export function fetchMovie(id) {
    const request = MDB.movies.details({append_to_response: "credits"}, {movie_id: id});

    return {
        type: FETCH_MOVIE,
        payload: request
    };
}
