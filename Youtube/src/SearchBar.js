import React, { Component } from 'react';
import { Button, Form, FormControl, Grid, Row, Col } from 'react-bootstrap';
import PropTypes from 'prop-types';

import './SearchBar.css';

class SearchBar extends Component {

    static propTypes = {
        onUserInput: PropTypes.func.isRequired
    }

    constructor(props) {
        super(props);
        this.state = {
            value: ''
        }
        this.handleChange = this.handleChange.bind(this);
        this.search = this.search.bind(this);
    }


    handleChange(e) {
        this.setState({ value: e.target.value });
    }

    search(e) {
        this.props.onUserInput(this.state.value);
    }

    render() {
        return (
            <Grid className='container'>
                <Row>
                    <Form method="GET" action=''>

                        <Col xs={12} md={6}>
                            <FormControl
                                type="text"
                                className='search-input'
                                value={this.state.value}
                                placeholder="Enter text"
                                onChange={this.handleChange}
                            />
                        </Col>
                        <Col xs={12} md={6}>
                            <Button
                                className="search-button"
                                bsStyle="primary"
                                onClick={this.search}>
                                Search
                        </Button>
                        </Col>
                    </Form>
                </Row>
            </Grid>
        );
    }
}

export default SearchBar;
