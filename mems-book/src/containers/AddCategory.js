import React, {Component} from 'react';
import { browserHistory} from 'react-router';
import {connect} from 'react-redux';
import {bindActionCreators} from 'redux';
import {addCategory} from '../actions'

class AddCategory extends Component {
     componentWillMount(){
        if (!localStorage.getItem('token')) {
             browserHistory.push('/');
        }
    }
    render() {
        let name, description
        return (
                <div ><br/>
 <div className="col-md-7 col-md-offset-2">
                    <form id="login-form"
                         onSubmit={e => {
                              e.preventDefault()
                              if (!name.value.trim() || !description.value.trim()) {
                                return
                              }
                             this.props.addCategory({name:name.value,description:description.value},
                                 localStorage.getItem('token')).then(()=> { browserHistory.push('/home')});
                            }}
                      >
                        <center><h2> <b>Add Category</b> </h2></center> <br/>


                          <div className="form-group">
                                <div className="row">
                                    <div className="col-md-12">
                                        <input type="text" placeholder="name" className=" form-control"
                                            ref={node => {
                                                    name = node
                                                  }}
                                        />
                                    </div>
                                </div>
                        </div>
                          <div className="form-group">
                            <div className="row">
                                <div className="col-md-12">
                                    <textarea type="description" placeholder="description" className="form-control"
                                    ref={node => {
                                        description = node;
                                        }}
                                    />
                                </div>
                            </div>
                        </div>

                        <div className="form-group">
                            <div className="row">
                                <div className="col-sm-6 col-sm-offset-3">
                                    <input type="submit" name="login-submit" tabIndex="4" className="btn btn-primary btn-block" value="Add Category"/>
                                </div>
                            </div>
                        </div>

                    </form>
                </div>
                </div>

                    );
    }
}


function mapDispatchToProps(dispatch){
    return bindActionCreators(
        {
            addCategory: addCategory
        }, dispatch);
}

export default connect(null, mapDispatchToProps)(AddCategory)











