// App.js

import React, {Component} from 'react';
import Search from '../containers/Search';
import Visualization from '../containers/Visualization';
const ReactHighcharts = require('react-highcharts');



class App extends Component {

    constructor(props) {
        super(props);
        this.state = {query:'',
            config:{}};
        // This binding is necessary to make `this` work in the callback
        this.handleChange = this.handleChange.bind(this);
        this.handleGraphConfig = this.handleGraphConfig.bind(this);
    }
    handleChange(event) {
        this.setState({query: event.target.value});
    }
    handleGraphConfig(data, title) {
        alert("a")
        console.log(data.temperature)
        this.setState({

        })
    }

    render() {
        return (
            <div className="container">
                <Search></Search>
                <Visualization
                    onGraphConfig={this.handleGraphConfig}
                ></Visualization>

            </div>
        )
    }
}

export default App;






