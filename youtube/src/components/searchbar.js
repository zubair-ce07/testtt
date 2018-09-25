import React from 'react';

class SearchBar extends React.Component{
  constructor(props){
    super(props);
    this.state = {search_term: ''};
    this.handleInputChange = this.handleInputChange.bind(this);
    this.searchOnClick =  this.searchOnClick.bind(this);
    this.searchOnKeyPress = this.searchOnKeyPress.bind(this);
  }

  handleInputChange(event){
    this.setState({search_term: event.target.value});
  }

  searchOnClick(){
    this.props.onSearch(this.state.search_term);
  }

  searchOnKeyPress(target){
    if(target.charCode==13){
      this.props.onSearch(this.state.search_term);
    }
  }

  render(){
    return(
      <div className="d-flex justify-content-center">
            <div className="col-xs-4">
                  <input className="form-control"
                    value = {this.state.search_term}
                    onChange = {this.handleInputChange}
                    onKeyPress={this.searchOnKeyPress}
                  />
            </div>
            <button className="btn btn-secondary btn-sm ml-2 my-2 my-sm-0"
              onClick={this.searchOnClick}>
              Search
            </button>
      </div>
    );
  }
}

export default SearchBar;
