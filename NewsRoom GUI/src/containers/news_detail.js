import React, { Component } from 'react';
import { connect } from 'react-redux';
import { fetchNewsDetail } from '../actions';
import _ from 'lodash';
import { Thumbnail, Jumbotron, Panel } from 'react-bootstrap';
import SearchBar from '../components/search_bar'


class NewsDetail extends Component {
    componentDidMount() {
        const id = this.props.match.params.id;
        this.props.fetchNewsDetail(id);
    }

    render() {
        const { selectedNews } = this.props;
        if (_.isEmpty(selectedNews)){
            return <div>Loading ....</div>
        }
        return (
            <div>
                <SearchBar />
                <Jumbotron>
                    <Thumbnail src={ selectedNews.image_url } alt="Image Not Availaible">
                        <div className="center-content">
                            <h1>{ selectedNews.title }</h1>
                            <div>
                                { selectedNews.published_date } | { selectedNews.category.name}
                            </div>
                            <h2>Summary</h2>
                            <p>{ selectedNews.summary }</p>
                        </div>
                    </Thumbnail>
                </Jumbotron>
            </div>
        );
    }
}
function mapStateToProps({ selected_news }, ownProps) {
    return { selectedNews:  selected_news};
}

export default connect(mapStateToProps, { fetchNewsDetail })(NewsDetail);