import React,{Component} from 'react'
import Multiselect from 'react-bootstrap-multiselect';


class someReactComponent extends Component {

    constructor(props){
      super(props);
      this.state = {test_data : [{value:'One', selected:false},{value:'Two', selected:false},{value:'three', selected:false},{value:'four', selected:false}]}
    }
    handleChange(object){
      console.log("Handle Object", object.context.value);
      console.log("Handle selected", object.context.selected);
    }

    render () {

        console.log("Test Data", this.state.test_data);
        return (
            <Multiselect onChange={this.handleChange.bind(this)} id="example-onChange" data={this.state.test_data} ref='ref' multiple/>
        );
    }
}

export default someReactComponent;


// var React = require('react');
// var Multiselect = require('react-bootstrap-multiselect');
//
// var someReactComponent = React.createClass({
//     getInitialState: function(){
//         var that = this;
//         $("element").on("event", function(){
//             $.get("new-data-from-url", function(newData){
//                 that.setState(newData);
//
//                 // to sync manually do
//                 that.refs.myRef.syncData();
//             });
//         });
//
//         return {
//             myData : [{value:'One',selected:true},{value:'Two'},{value:'3'},{value:'4'},{value:'5'},{value:'seven'}]
//         };
//     },
//     render: function () {
//         return (
//             <Multiselect onChange={this.handleChange} ref="myRef" data={this.state.myData} multiple />
//         );
//     }
// });
// export default someReactComponent;
