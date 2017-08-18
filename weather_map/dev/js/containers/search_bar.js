import React from 'react';
import { Navbar, FormGroup, FormControl,
         Button } from 'react-bootstrap';
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';
import { fetchWeather } from "../actions/fetch_weather";


class SearchBar extends React.Component
{
    constructor(props)
    {
        super(props);
        this.handleChange = this.handleChange.bind(this);
        this.search = this.search.bind(this);

        this.state = {query: ''};
    }

    handleChange(e)
    {
        this.setState({query: e.target.value});
    }

    search(e)
    {
        e.preventDefault();
        if(this.state.query)
        {
            this.props.fetchWeather(this.state.query);
            this.setState({query: ''});
        }
    }

    render()
    {
        return (
            <form onSubmit={this.search}>
                <Navbar.Form>
                    <FormGroup>
                        <FormControl type="text" onChange={this.handleChange}
                                     value={this.state.query} placeholder="Search" />
                        <Button type="submit" onClick={this.search}>Search</Button>
                    </FormGroup>
                </Navbar.Form>
            </form>
        )
    }
}

function mapDispatchToProps(dispatch)
{
    return bindActionCreators({ fetchWeather }, dispatch);
}

export default connect(null, mapDispatchToProps)(SearchBar);