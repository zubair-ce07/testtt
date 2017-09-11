import React from "react";
import NewsCard from "./NewsCard";
import {domain, getHeader} from "../config";

class News extends React.Component {
    static isPrivate = true;

    constructor(props) {
        super(props);
        this.state = {
            news: []
        };
        this.fetchNewsFromApi();
    }

    fetchNewsFromApi() {
        fetch(domain + '/news/', {
            method: 'GET',
            headers: getHeader()
        })
            .then((response) => response.json())
            .then((responseJson) => {
                if (responseJson) {
                    this.setState({
                        news: responseJson

                    });
                }
            })
            .catch((error) => {
                console.error(error);
            });
    }

    render() {
        let newsComponents = this.state.news.map((news) => <NewsCard key={news.id} news={news}/>);
        return (
            <div>
                <h3>News</h3>
                {newsComponents}
            </div>
        );
    }
}

export default News;
