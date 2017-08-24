import { combineReducers } from 'redux';
import MovieReducer from './movies_list';
import DetailedMovieReducer from './movie_detail';
import ActorReducer from './actor_detail';

const rootReducer = combineReducers(
    {
        movies: MovieReducer,
        detailed_movie: DetailedMovieReducer,
        actor: ActorReducer
    }
);

export default rootReducer;
