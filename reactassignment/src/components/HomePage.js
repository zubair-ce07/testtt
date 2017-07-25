import React from 'react'
// import {withRouter} from 'react-router-dom'
import {Jumbotron, Button} from 'react-bootstrap/lib'

class CustomJumbotron extends React.Component {
    constructor(props)
    {
        super(props)
    }
    render(){
        return (
        <Jumbotron>
            <h1>TODO, App!</h1>

            <p>This app lets you manage your daily tasks. {alert(this.props.c)}</p>

            <p> Simply add a list of tasks, and later check them as you
                accomplish your daily goals or delete the tasks holding you back!</p>

            <p>
                <Button bsStyle="primary" onClick={() => this.props.history.push('/home')}>Learn more</Button>
            </p>
        </Jumbotron>
    )
    }
}

export default CustomJumbotron
