import React from "react"
import {Paper} from "@material-ui/core/"



export default class Index extends React.Component {
    render() {
        return (
            <div>
                <Paper className="paper-style">
                    <h1>Welcome to Weatherman</h1>

                    <h3>Please select a city form sidebar to get started</h3>
                </Paper>
            </div>
        )
    }
}