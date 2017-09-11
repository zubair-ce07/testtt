import React from "react";
import {Media} from "react-bootstrap";
import {domain, getHeader} from "../config";

class NewsDetailedCard extends React.Component {
    render() {
        return (
            <div className="news-card" key={this.props.news.id}>
                <h1>{this.props.news.title}</h1>
                <Media>
                    <Media.Left>
                        <img src={this.props.news.image_url} alt="News"/>
                    </Media.Left>
                    <Media.Body>
                        <p dangerouslySetInnerHTML={{__html: this.props.news.content}}/>
                        <p>{this.props.news.pub_date}</p>
                    </Media.Body>
                </Media>
            </div>
        );
    }
}

export default class NewsDetailed extends React.Component {
    static isPrivate = true;

    constructor(props) {
        super(props);
        this.state = {};
        this.fetchNewsFromApi();
    }

    updateNewsState = (news) => {
        if (news) {
            this.setState({
                news: news,
            });
        }
    };

    fetchNewsFromApi = () => {
        fetch(domain + '/news/' + this.props.match.params.id, {
            method: 'GET',
            headers: getHeader(),
        })
            .then((response) => response.json())
            .then((responseJson) => {
                this.updateNewsState(responseJson);
            })
            .catch((error) => {
                console.error(error);
            });
    };

    render() {
        let newsComponent = this.state.news ? <NewsDetailedCard news={this.state.news}/> : null;
        return (
            <div>{newsComponent}</div>
        );
    }
}
