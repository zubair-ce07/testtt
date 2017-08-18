import React from "react";
import Header from "./Header";

class News extends React.Component {
    static isPrivate = true;

    render() {
        return (
            <div>
                <Header/>
                <h3>Oh Wow Too many news</h3>
            </div>
        );
    }
}

export default News;
