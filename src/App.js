import React, { Component } from 'react';
import './App.css';
import Player from './Player';
import List from './List';
import Search from './Search';
import { Route } from 'react-router-dom'

class App extends Component {

    constructor(props) {
        super(props);

        this.state = {
            query:'',
            items:[],
            searchText:'',
            fetchInProgress:false,
            message:''

        };

        this.handleChangeSearch = this.handleChangeSearch.bind(this);
        this.handleClickSearch = this.handleClickSearch.bind(this);
        this.handleDataRetrieval = this.handleDataRetrieval.bind(this);
        this.handleLoading = this.handleLoading.bind(this);

    }
    handleChangeSearch(query) {
        this.setState({query: query});
    }
    handleClickSearch() {

        this.setState({searchText: this.state.query});
    }
    handleDataRetrieval(items) {

        this.setState({items: items, fetchInProgress:false, message:''});
    }
    handleLoading(flag, message) {

        this.setState({fetchInProgress: flag, message:message});
    }


    render() {

        return (
            <div>
                <Route path='/'   render={()=>
                    <Search query={this.state.query}
                            onSearchChange={this.handleChangeSearch}
                            onSearchClick={this.handleClickSearch}/>}
                />
                <Route path='/search/:query' render={() =>
                    <List
                        items={this.state.items}
                        query={this.state.query}
                        fetchInProgress={this.state.fetchInProgress}
                        searchText={this.state.searchText}
                        onDataRetrieval={this.handleDataRetrieval}
                        onLoading={this.handleLoading}  />}
                />
                <Route path='/play/:id' component={Player}/>
                <div>
                    {(() => {
                        switch(this.state.fetchInProgress) {
                            case true:
                                return <div className={'alert-info'}>{this.state.message}</div>;
                            case false:
                                return <div className={'alert-danger'}>{this.state.message}</div>;
                            default: return null
                        }
                    })()}
                </div>

            </div>
        );
    }
}
export default App;