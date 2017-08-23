import TheMovieDatabase from 'themoviedatabase';

export const FETCH_MOVIES = 'FETCH_MOVIES';
export const FETCH_MOVIE = 'FETCH_MOVIE';

const MDB = new TheMovieDatabase('7b43db1b983b055bffd7534a06cafd6c');

export function fetchMovies() {
    const request = MDB.movies.nowPlaying();

    return {
        type: FETCH_MOVIES,
        payload: request
    };
}
export function fetchMovie(id) {
    const request = MDB.movies.details({append_to_response: "credits,videos"}, {movie_id: id});

    return {
        type: FETCH_MOVIE,
        payload: request
    };
}
