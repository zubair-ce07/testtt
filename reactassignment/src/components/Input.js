import React from 'react'


class InputTODO extends React.Component{

    _handleKeyUp(e){
        if(e.keyCode === 13){
            this.props.onAddClick()
        }
    }

    render()
    {
        return(
            <div>
                <hr/>
                <div className="text-center">
                    <input id="inputBox" type="text" onChange={this.props.onChange} onKeyUp={this._handleKeyUp.bind(this)}/>
                    <input type="button" value="Add+" onClick={this.props.onAddClick}></input>
                </div>
                <br/><br/><br/>
            </div>
        )
    }
}


export default InputTODO
