import React from 'react';
import { Navbar, FormGroup, FormControl,
         Button } from 'react-bootstrap'


class SearchBar extends React.Component
{
    render()
    {
        return (
            <form onSubmit={this.search}>
                <Navbar.Form>
                    <FormGroup>
                        <FormControl type="text" onChange={this.props.setQuery}
                         value={this.props.query} placeholder="Search" />
                    </FormGroup>
                    {' '}
                    <Button type="submit" onClick={this.props.search}>Search</Button>
                </Navbar.Form>
            </form>
        );
    }
}

export default SearchBar;