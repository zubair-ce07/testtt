import React from 'react';
import TimeAgo from 'react-timeago';
import { connect } from 'react-redux';
import { Link } from 'react-router';
import { RetrieveSingleNews } from "../actions/RetrieveSingleNews";
import _ from "lodash";

class NewsDetail extends React.Component {
    componentWillMount()
    {
        window.scrollTo(0,0);
        this.props.RetrieveSingleNews(this.props.params.id)
    }

    displayNews = (news) => {
        return(
            <div>
                <Link to={'/news'} className={ "btn btn-primary" }> Back </Link>
                <a href={ news.link }><h3>{ news.title }</h3></a>
                <img className={"img-rounded"} src={ news.image_url } alt={'Light'}/>
                <br/>
                <label>Author: <span>{ news.author_name }</span></label>
                <br/>
                <label>Published: <TimeAgo date={news.date} /></label>
                <br/><br/>
                <label>Details:</label>
                <p>{ news.detail }</p>
                <br/>
            </div>
        )
    };
    render()
    {
        if(_.isEmpty(this.props.news)){
            return <h1>News Not Found</h1>
        }
        return this.displayNews(this.props.news)
    }
}
function mapStateToProps(state)
{
    return {news: state.newsDetailReducer.selectedNews.data };
}

export default connect(mapStateToProps,{ RetrieveSingleNews })(NewsDetail);