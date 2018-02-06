import React from "react";
import ContentEditable from 'react-sane-contenteditable'
import Service from './Service.jsx';

export default class Profile extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            html:{heading: ""}
        }
        this.handleChange = this.handleChange.bind(this);
    }
    handleChange(event, value){
      console.log("change",value);
      console.log("event", event.target);
      // const field = event.target.id;
      // const html = this.state.html;
      // html[field] = value;
      // this.setState({
      //    html
      // });
      //  console.log("changed",this.state.html.heading);
    }
    edit(event, value){
      console.log("change",value);
      console.log("event", event);
      const field = event.target.id;
      const html = this.state.html;
      html[field] = value;
      this.setState({
         html
      });
       console.log("changed",this.state.html.heading);
    }
    renderServices(){
        const services = []
        for (var i = 6 - 1; i >= 0; i--) {
            services.push(<Service id={i}/>)
        }
        return services;
             
    }
    render() {
        return (
            <div className="container">
                <div className="single">  
                    <div className="row">
                        <div className="col-md-offset-10 col-md-2">
                            <a href="#" className="btn btn-primary btn-default btn-lg"><i className="fa fa-edit">Edit</i></a>
                        </div>
                    <div className="box_1">
                        <h3>What we do</h3>
                        <div className="col-md-12 service_box1">
                            <div className="row">
                                <div>
                                    <div className="col-md-10">
                                        <h5 contentEditable="true" id="heading"  onChange={this.handleChange}></h5>
                                    </div>
                                </div>
                            </div>
                            <div className="row">
                                <div>
                                    <div className="col-md-10">
                                         <ContentEditable
                                              html={this.state.html.description}
                                              tagName="p"
                                              id="description"
                                              onChange={ this.handleChange }
                                              contentEditable="plaintext-only"
                                            />
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div className="clearfix"> </div>
                    </div>
                    <div className="box_2">
                        <h3>Tags</h3>
                            {this.renderServices()}
                        <div className="clearfix"> </div>
                    </div>
                </div>
            </div>
        </div>
        );
    }
}
