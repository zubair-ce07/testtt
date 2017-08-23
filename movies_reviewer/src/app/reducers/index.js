import { combineReducers } from 'redux';
import MovieReducer from './movies_list';
import DetailedMovieReducer from './movie_detail';


const rootReducer = combineReducers(
    {
        movies: MovieReducer,
        detailed_movie: DetailedMovieReducer
    }
);

export default rootReducer;
