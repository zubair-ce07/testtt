import React from 'react';
import TimeAgo from 'react-timeago';
import { connect } from 'react-redux';
import { browserHistory } from 'react-router'
import Navbar from '../components/Navbar'
import { RetrieveSingleNews } from "../actions/RetrieveSingleNews";
import _ from "lodash";

class NewsDetail extends React.Component {
    componentWillMount()
    {
        if(!localStorage.getItem('token')){
            browserHistory.push('/')
        }
        else {
            window.scrollTo(0,0);
            this.props.RetrieveSingleNews(this.props.params.id)
        }
    }

    displayNews = (news) => {
        return(
            <div>
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
        return<div><Navbar/>{this.displayNews(this.props.news)}</div>
    }
}
function mapStateToProps(state)
{
    return {news: state.newsDetailReducer.selectedNews.data };
}

export default connect(mapStateToProps,{ RetrieveSingleNews })(NewsDetail);
