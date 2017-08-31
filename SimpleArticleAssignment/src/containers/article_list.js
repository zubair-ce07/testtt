import React, { Component } from 'react';
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';

import { selectArticle, getArticleList } from '../actions/index'

class ArticleList extends Component{

    constructor(props){
        super(props);
        this.props.getArticleList();

    }

    renderArticleList(){
        return this.props.articles.map(article =>{
            return(
              <li
                  onClick={() => this.props.selectArticle(article)}
                  key={article.id}
                  className="list-group-item "
              >
                  {article.title}
              </li>
            );
        });
    }//renderList

    render(){
        return(
            <ul
                className="list-group col-sm-4"
            >
                { this.renderArticleList() }
            </ul>
        );
    }//render

}//class

function mapStateToProp(state){
    return(
        {
            articles: state.articles
        }
    );
}//function


function mapDispatchToProp(dispatch) {
    return bindActionCreators (
        {
            selectArticle:selectArticle,
            getArticleList:getArticleList
        },
        dispatch
    );
}//mapDispatchToProp

export default connect (mapStateToProp, mapDispatchToProp)(ArticleList);

