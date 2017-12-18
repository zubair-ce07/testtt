import {combineReducers} from 'redux';
import {reducer as formReducer} from 'redux-form';

import ActorReducer from './actor_detail';
import DetailedMovieReducer from './movie_detail';
import MovieReducer from './movies_list';
import ReviewsReducer from './reviews_list';

const rootReducer = combineReducers({
    movies: MovieReducer,
    detailed_movie: DetailedMovieReducer,
    actor: ActorReducer,
    reviews: ReviewsReducer,
    form: formReducer
});

export default rootReducer;
