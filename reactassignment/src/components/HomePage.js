import React from 'react'
import {Jumbotron, Button} from 'react-bootstrap/lib'

class CustomJumbotron extends React.Component {
    constructor(props)
    {
        super(props)
        console.log(this.props)
    }
    render(){
        return (
        <Jumbotron>
            <h1>TODO, App!</h1>

            <p>This app lets you manage your daily tasks. {console.log(this.props.count)}</p>

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
