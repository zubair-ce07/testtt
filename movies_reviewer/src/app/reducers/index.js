import { combineReducers } from 'redux';
import { reducer as formReducer } from 'redux-form';

import MovieReducer from './movies_list';
import DetailedMovieReducer from './movie_detail';
import ActorReducer from './actor_detail';
import ReviewsReducer from './reviews';

const rootReducer = combineReducers(
    {
        movies: MovieReducer,
        detailed_movie: DetailedMovieReducer,
        actor: ActorReducer,
        reviews: ReviewsReducer,
        form: formReducer
    }
);

export default rootReducer;
