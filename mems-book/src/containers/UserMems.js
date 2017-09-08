import React, {Component} from "react";
import {browserHistory} from "react-router";
import {connect} from "react-redux";
import {bindActionCreators} from "redux";
import {getUserMems} from "../actions";
import Memory from "../components/Mem";

class UserMems extends Component {
    componentWillMount() {
        if (localStorage.getItem('token')) {
            this.props.getUserMems(localStorage.getItem('token'));
        } else {
            browserHistory.push('/');
        };
    };
    renderAllMems() {
        return this.props.user_mems.map((mem) => {
            return <Memory key={mem.id} mem={mem}/>
        });
    };
    render() {
        return (
            <div>
                <center><h2><b>Your Mems</b></h2></center>
                <br/>
                {this.renderAllMems()}
            </div>
        );
    };
};
function mapStateToProps(state) {

    return {
        user_mems: state.user_mems
    };
};
function mapDispatchToProps(dispatch) {
    return bindActionCreators({
            getUserMems: getUserMems,
        }, dispatch);
};
export default connect(mapStateToProps, mapDispatchToProps)(UserMems);
