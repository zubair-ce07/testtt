import React, { Component } from 'react';
import { connect } from 'react-redux';

class SelectedArticle extends Component{

    render(){
        let selectedArticle = this.props.selectedArticle;

        if (!selectedArticle){
            return <h1> Select Article To View Detail. </h1>
        }
        return(
            <div>
                <h1 className="h1">
                    {selectedArticle.title}
                </h1>
                <div>
                    <strong>Category Name: </strong>
                    {selectedArticle.category_name}
                </div>
                <div>
                    <strong>Category Source: </strong>
                    {selectedArticle.category_source}
                </div>
                <div>
                    <strong>Publication date: </strong>
                    {selectedArticle.publication_date}
                </div>
                <div>
                    <strong>Tags: </strong>
                    {selectedArticle.tags}
                </div>
                <br/>
                <div>
                    <strong>Detail: </strong>
                    {selectedArticle.detail}
                </div>
            </div>
        );
    }//render

}//class

function mapStateToProp(state){
    return(
        {
            selectedArticle: state.selectedArticle
        }
    );
}//function

export default connect (mapStateToProp)(SelectedArticle);
