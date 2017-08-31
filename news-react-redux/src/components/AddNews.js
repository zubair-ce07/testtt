import React from 'react';
import AddNewsForm from "./AddNewsForm";
import {connect} from "react-redux";


const mapStateToProps = (state) => {
    return {
        onSubmit: () => {
            alert(state.form);
        }
    }
};

const AddNewsContainer = connect(
    mapStateToProps
)(AddNewsForm);

export default class AddNews extends React.Component {
    static isPrivate = true;

    render() {
        return (
            <AddNewsContainer/>
        )
    }
}
