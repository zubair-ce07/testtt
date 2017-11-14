import React from 'react'


const InputTODO = (props) => {
    return(
            <div>
                <hr/>
                <div className="text-center">
                    <input
                        id="inputBox"
                        type="text"
                        onChange={props.onChange}
                        onKeyUp={(e) => (e.keyCode === 13 ? props.onAddClick():{})}
                    />
                    <input type="button" value="Add+" onClick={props.onAddClick}></input>
                </div>
                <br/><br/><br/>
            </div>
        )
}




export default InputTODO
