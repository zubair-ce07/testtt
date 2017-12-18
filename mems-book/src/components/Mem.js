import React, {Component} from "react";
import {connect} from "react-redux";
import {browserHistory} from "react-router";
import {deleteMem} from "../actions";

class Memory extends Component {
    rederControles() {
        if (this.props.mem.user == JSON.parse(localStorage.getItem('user')).id) {
            return (
                <div className="card-action">
                    <button className="btn1 btn-danger" onClick={
                        (e) => {
                            e.preventDefault();
                            this.props.deleteMem(this.props.mem.id, localStorage.getItem('token'));
                        }}> Delete </button>{" "}
                    <button className="btn1 btn-info" onClick={
                        (e) => {
                            e.preventDefault();
                            browserHistory.push(`editmem${this.props.mem.id}`)
                        }}>Edit</button>
                </div>);
        } else {
            return <div className="card-action">
                        <p><a href={this.props.mem.url}>Reference Link Is Here</a></p>
                    </div>
        }
    };
    renderLink() {
        if (this.props.mem.user == JSON.parse(localStorage.getItem('user')).id) {
            return <p><a href={this.props.mem.url}>Reference Link Is Here</a></p>;
        };
    };
    render() {
        return (
            <div className="col-md-4 col-sm-4">
                <div className="card">
                    <div className="card-image  waves-effect waves-block waves-light">
                        <img className="activator mem-image" src={this.props.mem.image}/>
                    </div>
                    <div className="card-content">
                        <h3><b> {this.props.mem.title }</b></h3>
                        <p>{ this.props.mem.text }</p>
                        {this.renderLink()}
                    </div>
                    {this.rederControles()}
                </div>
            </div>
        );
    };
};
export default connect(null, {deleteMem: deleteMem})(Memory);
