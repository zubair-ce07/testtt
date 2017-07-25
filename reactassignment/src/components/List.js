import React from 'react'
import {ListGroup, ListGroupItem, Checkbox, Glyphicon} from 'react-bootstrap/lib'
class ListTODO extends React.Component {

    _delete_task(e)
    {
        this.props.onDeleteTask(e)
    }

    _checkbox_clicked(e) {
        this.props.onCheckClick(e)
    }

    is_pending(task) {
        if (task.pending)
            return task.subject
        else
            return <del>{task.subject}</del>
    }
    render() {
        const divstyle = {
            float: 'right',
            margin: 'auto'
        }
        let addedTasks = []

        let handle_click = this._checkbox_clicked.bind(this)
        let handle_delete = this._delete_task.bind(this)
        let _is_pending = this.is_pending.bind(this)


        this.props.taskList.forEach(function (task) {
                if (task) {
                    let subject = _is_pending(task)
                    let index = task.index
                    addedTasks.push(
                        <ListGroupItem>
                            {subject}
                            <Glyphicon
                                style={divstyle}
                                glyph='trash'
                                bsSize='small'
                                onClick= {() => handle_delete(index)} />
                            <Checkbox style={divstyle} value={task.index} onClick={handle_click}/>

                        </ListGroupItem>
                    )
                }
            });
        return (
            <ListGroup>
                {addedTasks}
            </ListGroup>
        )
    }
}

export default ListTODO
