import React, {Component} from 'react';
import ReactDOM from 'react-dom';
import MovieDB from 'moviedb';

import SearchBar from './components/search_bar';
import MovieList from './components/movie_list';
import MovieDetail from './components/movie_detail';


const MDB = MovieDB('7b43db1b983b055bffd7534a06cafd6c');


class App extends Component {
    constructor(props) {
        super(props);

        this.state = {
            movies: [],
            selectedMovie: null
        };
        this.movieSearch('');
    }

    movieSearch(term) {
        if(term === '')
            MDB.miscNowPlayingMovies({}, (err, res) => this.updateState(res.results, res.results[0]));
        else
            MDB.searchMovie({query: term},(err, res) => this.updateState(res.results, res.results[0]));
    }

    updateState(movies, selectedMovie){
        this.setState({ movies, selectedMovie});
    }

    render() {

        return (
            <div>
                <SearchBar onSearchTermChange={term => this.movieSearch(term)}/>
                <div className="row">
                    <MovieDetail movie={this.state.selectedMovie}/>
                    <MovieList onMovieSelect={selectedMovie => this.setState({selectedMovie}) }
                               movies={this.state.movies}/>
                </div>
            </div>
        );
    }
}

ReactDOM.render(<App/>, window.document.getElementById('app'));
