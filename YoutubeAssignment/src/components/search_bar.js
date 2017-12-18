import React, {Component} from 'react';

class SearchBar extends Component{
    constructor(props){
        super(props);
        this.onSubmit = this.onSubmit.bind(this);
        this.state = {'queryText': ''}
    }//contructor

    render(){
        return(
            <div>
                <form onSubmit={this.onSubmit} className="input-group col-sm-6">
                    <input
                        className="search-bar col-sm-12"
                        placeholder="Search Youtube Videos here"
                        value = {this.state.queryText}
                        onChange ={ event => this.onTextChange(event.target.value)}
                    />
                    <span className="input-group-btn">
                        <button type="submit" className="btn btn-default">Search</button>
                    </span>
                </form>
            </div>
        );
    }//render

    onTextChange(queryText){
        this.setState({queryText});
    }

    onSubmit(event){
        event.preventDefault();
        this.props.onQueryChange(this.state.queryText);
    }

}//class

export default SearchBar;
