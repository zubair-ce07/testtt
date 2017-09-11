import React from "react";
import PropTypes from 'prop-types'
import VisibleNewsList from "./VisibleNewsList";
import {refreshState, setUser} from "../actions/storeAction";
import {loadNewsFromAPI} from "../actions/index";


class Home extends React.Component {
    static isPrivate = false;

    componentWillMount = () => {
        const {store} = this.context;
        store.dispatch(refreshState());
        store.dispatch(setUser(
            localStorage.username, localStorage.authToken));
        loadNewsFromAPI(store);
    };

    render() {
        return (
            <div>
                <VisibleNewsList/>
            </div>
        );
    }
}

Home.contextTypes = {
    store: PropTypes.object,
};

export default Home;