/**
 * Created by mzulqarnain on 1/30/18.
 */
import React from "react";
import SearchForm from "./Search";
import axios from "axios";
import {API_CALL, API_KEY, COUNTRY_NAME, NO_CITY_MSG} from "./constants";
import ResultList from './ResultList'

class Root extends React.Component {

    constructor() {
        super();
        this.state = {
            cityName: '',
            error: '',
            data: []
        };
        this.onChangeName = this.onChangeName.bind(this);
        this.onSubmit = this.onSubmit.bind(this);
        this.get5DaysWeather = this.get5DaysWeather.bind(this);
    }

    get5DaysWeather(cityName) {

        let full_uri = `${API_CALL}?q=${cityName},${COUNTRY_NAME}&appid=${API_KEY}`;

        return axios.get(full_uri)
          .then(response => this.setState({data: response.data.list}))
            .catch(error => this.setState({data: [], error: NO_CITY_MSG}));
    }

    onChangeName(event) {
        this.setState({cityName: event.target.value});
    }

    onSubmit() {
        this.setState({error: ''});
        this.get5DaysWeather(this.state.cityName);
        console.log(this.state.data)
    }

    render() {
        let weather = null;
        if(this.state.data){
            weather = <ResultList city={this.state.cityName} data={this.state.data}/>
        }

        return (
                <div>
                    <SearchForm cityName={this.state.cityName}
                                error={this.state.error}
                                onChangeName={this.onChangeName}
                                onSubmit={this.onSubmit}
                    /><br/><br/>
                    {weather}
                </div>
        )
    }
}

export default Root;