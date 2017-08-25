import _ from 'lodash';
import Rating from 'react-rating';
import {connect} from 'react-redux';
import React, {Component} from 'react';
import {Field, reduxForm} from 'redux-form';

import {addReview, fetchReviews} from '../actions/index';

class NewReview extends Component {
    componentWillMount() {
        this.props.fetchReviews(this.props.match.params.movie_id);
    }

    onSubmit(props) {
        props["movie_id"] = this.props.match.params.movie_id;
        this.props.addReview(props, () => this.props.reset());
    }

    static renderField(field) {
        let input = <Rating {...field.input} initialRate={parseFloat(field.input.value)} fractions={2}/>;
        if (field.type === "text")
            input = <textarea {...field.input} className="form-control"/>;
        return (
            <div className={`form-group ${field.meta.touched && field.meta.invalid ? 'has-danger' : ''}`}>
                <label>{field.label}</label><br/>
                {input}
                <div className="text-danger">
                    {field.meta.touched ? field.meta.error : ''}
                </div>
            </div>
        );
    }

    renderReviews() {
        const reviews = _.values(this.props.reviews).reverse();
        return reviews.map((review) => {
            return (
                <li className="list-group-item" key={review.id}>
                    <p>Rating: {review.rating}</p>
                    <h6>Comment: {review.comment}</h6>
                </li>
            );
        });
    }

    render() {
        return (
            <div>
                <h1 className="page-title">Reviews</h1>
                <div className=" row top-element">
                    <div className="col-md-4"/>
                    <div className="col-md-4">
                        <form onSubmit={this.props.handleSubmit(this.onSubmit.bind(this))}>
                            <Field label="Rating" name="rating" component={NewReview.renderField}/>
                            <Field label="Comment" type="text" name="comment" component={NewReview.renderField}/>
                            <button type="submit" className="btn btn-primary">Add Review</button>
                        </form>
                    </div>
                </div>
                <br/>
                <div className="row">
                    <div className="col-md-4"/>
                    <div className="col-md-4">
                        <ul className="list-group">{this.renderReviews()}</ul>
                    </div>
                </div>
            </div>
        );
    }
}

function validate(values) {
    const errors = {};
    if (!values.rating) {
        errors.rating = 'Select some rating';
    }
    if (!values.comment) {
        errors.comment = 'Add some comment';
    }
    return errors;
}

function mapStateToProps({reviews}, ownProps) {
    const props = {reviews: {}};
    if (reviews && reviews.movie_id === Number(ownProps.match.params.movie_id))
        props["reviews"] = reviews.rev_list;
    return props;
}

export default reduxForm({form: 'ReviewsNewForm', validate})(
    connect(mapStateToProps, {addReview, fetchReviews})(NewReview)
);
