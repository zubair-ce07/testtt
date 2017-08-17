import React, { Component } from 'react';
import MemoryAPI from './MemoryAPI'


export  default class AddMemory extends Component{
    constructor(props){
        super(props);
        this.state = {title:'',
            category:'',
            text:'',
            tags:'',
            url:'',
            is_public:true
        }
        this.handleInputChange = this.handleInputChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleInputChange(event) {
        const elem = event.target;
                const val = elem.name === 'is_public' ? elem.checked : elem.value;
                this.setState({
                    [elem.name]: val
                });
    }
    handleSubmit(event){
        new MemoryAPI().addMemory(this.state).then(alert('Added Successfully'));
        event.preventDefault();
    }

    render(){
        return (
                <form onSubmit={this.handleSubmit}>
                    <input type="text" name="title" placeholder="Title" value={this.state.title} onChange={this.handleInputChange} /><br/>
                    <input type="text" name="category" placeholder="Category" value={this.state.category} onChange={this.handleInputChange}/><br/>
                    <input type="text" name="text" placeholder="Text of Mem" value={this.state.text} onChange={this.handleInputChange}/><br/>
                    <input type="text" name="tags" placeholder="Tags" value={this.state.tags} onChange={this.handleInputChange}/>
                    <input type="text" name="url" placeholder="URL" value={this.state.url} onChange={this.handleInputChange}/>
                    <p><input type="checkbox"  name="is_public" value={this.state.is_public}/> {' '} is public</p>
                    <input type="submit" value="Add Memory"/>
                </form>
        );
    }
}
