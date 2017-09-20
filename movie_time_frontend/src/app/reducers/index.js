import {combineReducers} from 'redux';
import {reducer as formReducer} from 'redux-form';

import ActivitiesReducer from './activities_reducer';
import SearchReducer from './search_reducer';
import NotificationsReducer from './notifications_reducer';
import AuthReducer from './auth_reducer';
import ToWatchListReducer from './to_watch_reducer';
import WatchedListReducer from './watched_reducer';
import UpcomingListReducer from './upcoming_reducer';
import CalendarReducer from './calendar_reducer';
import GenresReducer from './genres_reducer';
import GenreMoviesReducer from './genre_movies_reducer';
import ActivePageReducer from './active_page_reducer';
import MovieReducer from './movie_reducer';

const rootReducer = combineReducers({
    movie_detail: MovieReducer,
    active_page: ActivePageReducer,
    genre_movies_list: GenreMoviesReducer,
    genres_list: GenresReducer,
    released_on_list: CalendarReducer,
    upcoming_list: UpcomingListReducer,
    watched_list: WatchedListReducer,
    to_watch_list: ToWatchListReducer,
    search_results: SearchReducer,
    notifications: NotificationsReducer,
    activities: ActivitiesReducer,
    auth_user: AuthReducer,
    form: formReducer
});

export default rootReducer;
