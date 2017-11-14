import React from 'react'

import {ListGroupItem, Glyphicon, Checkbox} from 'react-bootstrap/lib'


class TodoItem extends React.Component{
    constructor(props){
        super(props)

        var {index, subject, pending} = this.props.task;
        console.log(index)
        var {handleCheckClick, handleDeleteTask} = this.props.handlers;


        this.index = index
        this.subject = subject
        this.pending = pending
        this.divstyle = {
            float: 'right',
            margin: 'auto'
        }
        this.handleCheckClick = handleCheckClick.bind(this)
        this.handleDeleteTask = handleDeleteTask.bind(this)
    }
    render(){
        return(

            <ListGroupItem key={this.index}>

                {(this.pending ? this.subject:(<del>{this.subject}</del>))}

                <Glyphicon
                    style={this.divstyle}
                    glyph='trash'
                    bsSize='small'
                    onClick= {(e) => this.handleDeleteTask(this.index)}
                />

                <Checkbox
                    style={this.divstyle}
                    value={this.index}
                    onClick={this.handleCheckClick}
                    defaultChecked={!this.pending}
                />

            </ListGroupItem>
        )
    }
}


export default TodoItem
