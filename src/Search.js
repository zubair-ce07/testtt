/**
 * Created by mzulqarnain on 1/30/18.
 */
import React from 'react'


class SearchForm extends React.Component{

    render(){
        return(
            <div>
                <label>Enter City Name</label><br/><br/>
                <input type="text" onChange={this.props.onChangeName}/><br/><br/>
                <span style={myStyle}>{this.props.error}</span><br/>
                <input type="submit" value="Submit" onClick={this.props.onSubmit}/>
            </div>
        )
    }
}

const myStyle = {
    color: 'red',
};

export default SearchForm;