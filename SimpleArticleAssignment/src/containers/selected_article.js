import React, { Component } from 'react';
import { connect } from 'react-redux';

class SelectedArticle extends Component{

    render(){
        if (!this.props.selectedArticle){
            return <h1> Select Article To View Detail. </h1>
        }

        return(
            <div>
                <h1 className="h1">
                    {this.props.selectedArticle.title}
                </h1>
                <div>
                    <strong>Category Name: </strong>
                    {this.props.selectedArticle.category_name}
                </div>
                <div>
                    <strong>Category Source: </strong>
                    {this.props.selectedArticle.category_source}
                </div>
                <div>
                    <strong>Publication date: </strong>
                    {this.props.selectedArticle.publication_date}
                </div>
                <div>
                    <strong>Tags: </strong>
                    {this.props.selectedArticle.tags}
                </div>
                <br/>
                <div>
                    <strong>Detail: </strong>
                    {this.props.selectedArticle.detail}
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

