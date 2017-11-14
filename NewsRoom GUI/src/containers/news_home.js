import React, { Component } from 'react';
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';
import { Grid, Row, Panel, Well} from 'react-bootstrap';
import _ from 'lodash';
import { fetchNewsTop, fetchNewsByCategories } from '../actions';
import SearchBar from '../components/search_bar'
import NewsSlider from '../components/news_slider';
import NewsThumbnailList from '../components/news_thumbnail_list';


class NewsHome extends Component {
    componentDidMount(){
        this.props.fetchNewsTop(3);
        this.props.fetchNewsByCategories(3);
    }

    renderOtherNews() {
        return this.props.otherNews.map((categoryObject) => {
            return (
                <Panel key={categoryObject.category}>
                    <Row>
                        <Well>
                            <h2>
                                <Link to={`/news/categories/${categoryObject.category}`}>{categoryObject.category}</Link>
                            </h2>
                        </Well>
                        <NewsThumbnailList news_list={categoryObject.news} />
                    </Row>
                </Panel>
            );
        })
    }

    render() {
        if (!this.props.topNews || _.isEmpty(this.props.otherNews)) {
            return <div>Loading ... </div>
        }
        return (
            <div>
                <SearchBar />
                <div className="object-center"><NewsSlider news={this.props.topNews}/></div>
                <Grid>
                    {this.renderOtherNews()}
                </Grid>
            </div>
        );
    }
}

function mapStateToProps(state) {
    return { 
        topNews: state.top_news,
        otherNews: state.otherNews
    };
}


export default connect(mapStateToProps, { fetchNewsTop, fetchNewsByCategories })(NewsHome);
