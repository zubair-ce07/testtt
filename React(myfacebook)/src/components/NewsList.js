import React from 'react';
import { Link } from 'react-router';
import { connect } from 'react-redux';
import { RetrieveNews } from '../actions/RetrieveNews';
import _ from "lodash";

class NewsList extends React.Component {
    componentWillMount(){
        this.props.RetrieveNews();
    }

    displayNewsList = (news) => {
        let imgStyle = {
            width: '100%',
            height: '195px'
        };

        let divThumbnailStyle ={
            height: '325px',
            textAlign: 'center'
        };

        let divTitleStyle = {
            height: '3em'
        };
        return (
            news.map(singleNews => {
                return(
                    <div className={"col-md-4"} key={singleNews.id}>
                        <div className={"thumbnail"} style={divThumbnailStyle} >
                            <div className={"title"} style={divTitleStyle}>
                                <strong>{ singleNews.title }</strong>
                            </div>
                            <Link to={`/news/${singleNews.id}`} activeClassName={'active'}>
                                <img src={ singleNews.image_url } alt={"Lights"} style={imgStyle} />
                                <div className={"caption"}>
                                    <p>{ singleNews.description }</p>
                                </div>
                            </Link>
                        </div>
                    </div>
                )
            })
        )
    };

    render()
    {
        if(_.isEmpty(this.props.news)){
            return <h1>Loading...</h1>
        }
        return <div>{this.displayNewsList(this.props.news)}</div>

    }


}
function mapStateToProps(state)
{
    return {news: state.newsListReducer.news.data };
}

export default connect(mapStateToProps,{ RetrieveNews })(NewsList);