import React, { Component } from 'react';
import PropTypes from 'prop-types'
import Memory from './Memory';
import MemoryAPI from './MemoryAPI';
import AddMemory from './AddMemory'

class MainPage extends Component{
    constructor(props){
        super(props);
         this.state = { mems: [] };
    }
    onNewMemoryAdd(memory){
        this.setState((prevState, props) => {prevState.mems.push(memory);{
            mems:prevState.mems
        }});
    }
    render(){
        let mems = this.state.mems.map(mem => {
             return <Memory mem={mem} key={mem.id}/>
        });
        return (
            <div>
                <div> <AddMemory onAdd={this.onNewMemoryAdd.bind(this)}/> </div>
                <div > {mems} </div>
            </div>
        );
    }
    componentDidMount(){
        new MemoryAPI().getAllMems().then(data => {this.setState({mems:data})});
    }
}
MainPage.propTypes = {
    mems : PropTypes.array
}

export default MainPage;
