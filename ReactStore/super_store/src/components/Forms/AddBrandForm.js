import React from 'react'
import PropTypes from 'prop-types'
import {Route} from 'react-router-dom'
import {Jumbotron, Button, FormControl,  HelpBlock, FormGroup, ControlLabel} from 'react-bootstrap/lib'

import Navigation from '../Common/Header'
import {createOrUpdateBrand} from '../authentication/auth'
import {getOrDeleteBrand} from '../authentication/auth'

var toastr = require('toastr');

function FieldGroup({ id, label, help, error, ...props }) {
  return (
    <FormGroup controlId={id}>
      <ControlLabel>{label}</ControlLabel>
      <FormControl {...props} />
      {error && <label className='text-danger'>{error}</label>}
      {help && <HelpBlock>{help}</HelpBlock>}
    </FormGroup>
  );
}

class AddBrandForm extends React.Component {
    constructor(props){
        super(props)
        this.state = {
            file: '',
            imagePreviewUrl: '',
            binaryString: '',
            linkError: '',
            nameError: '',
            imageError: '',
            brand: {}
        }
        this._handleSubmit = this._handleSubmit.bind(this)
        this._handleNameChange = this._handleNameChange.bind(this)
    }

    _handleNameChange(e){
        const brand = Object.assign({}, this.state.brand)
        brand[e.target.name] = e.target.value
        this.setState({
            brand
        })
    }

    componentDidMount(){
        if(this.props.match !== undefined){
            getOrDeleteBrand(this.props.match.params.id, 'get', jsonData => {
                console.log(jsonData)
                let brand = Object.assign({}, jsonData)
                this.setState({
                    brand,
                    imagePreviewUrl: brand.image_icon
                })
                console.log(this.state)
            })
        }
    }
    _handleImageChange(e) {
        e.preventDefault();

        let reader = new FileReader();
        let sreader = new FileReader();
        let file = e.target.files[0];

        reader.onloadend = () => {
            this.setState({
                file: file,
                imagePreviewUrl: sreader.result,
                binaryString: reader.result,
            });
        }
        sreader.readAsDataURL(file)
        reader.readAsBinaryString(file)
    }
    validateURL(textval) {
        const urlregex = /^(https?|ftp):\/\/([a-zA-Z0-9.-]+(:[a-zA-Z0-9.&%$-]+)*@)*((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9][0-9]?)(\.(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])){3}|([a-zA-Z0-9-]+\.)*[a-zA-Z0-9-]+\.(com|edu|gov|int|mil|net|org|biz|arpa|info|name|pro|aero|coop|museum|[a-zA-Z]{2}))(:[0-9]+)*(\/($|[a-zA-Z0-9.,?'\\+&%$#=~_-]+))*$/;
        return urlregex.test(textval);
    }
    _handleSubmit(e){
        e.preventDefault()
        let bool = false
        if(!this.validateURL(e.target.formControlsBrandLink.value.toString())){
            this.setState({linkError: 'Invalid URL'})
            bool = true
            document.getElementById('formControlsBrandLink').focus()
        }
        else{
            this.setState({linkError: ''})
        }
        if(this.state.imagePreviewUrl === ''){
            this.setState({imageError: 'Image is required!'})
            bool = true
        }
        if(e.target.formControlsBrandName.value.length === 0){
            this.setState({
                nameError: 'name of the brand is required'
            })
            if(!bool){
                document.getElementById('formControlsBrandName').focus()
            }
            bool = true
        }
        else{
            this.setState({nameError: ''})
        }
        if(bool){
            return false
        }
        let data = document.getElementById('brandCreate')
        if(this.props.match === undefined){
            createOrUpdateBrand(data, false, (jsonData) => {
                data.reset()
                this.setState({
                    file: '',
                    imagePreviewUrl: '',
                    binaryString: '',
                    linkError: '',
                    nameError: '',
                    imageError: '',
                    brand: {}
                })
                toastr.success('brand created successfully!')
            })
        }
        else{
            createOrUpdateBrand(data, true, (jsonData) => {
                this.setState({
                    file: '',
                    imagePreviewUrl: '',
                    binaryString: '',
                    linkError: '',
                    nameError: '',
                    imageError: '',
                    brand: jsonData
                })
                toastr.success('brand updated successfully!')
            })
        }
    }
    render(){
        const {imagePreviewUrl} = this.state;
        let $imagePreview = null;
        if (imagePreviewUrl) {
            $imagePreview = (<img src={imagePreviewUrl} alt="Brand" />);
        }
        return (
            <div>
                {this.props.match !== undefined ? <Route component={Navigation} />:''}
                <Jumbotron>
                    <div className='container'>
                        <h1>{this.props.match === undefined ? 'Add A New Brand!!':'Update This Brand!!'}</h1>
                        <form id="brandCreate" encType='multipart/form-data' onSubmit={this._handleSubmit}>
                            <input type="hidden" value={this.state.brand.pk || ''} name='pk'/>
                            <FieldGroup
                                id="formControlsBrandName"
                                type="text"
                                label="Brand Name"
                                placeholder="Enter brand name"
                                name="name"
                                error={this.state.nameError}
                                value={this.state.brand.name || ''}
                                onChange={this._handleNameChange}
                            />
                            <FieldGroup
                                id="formControlsBrandLink"
                                type="text"
                                label="Brand Page's Link"
                                placeholder="Enter brand website Link"
                                name="brand_link"
                                error={this.state.linkError}
                                value={this.state.brand.brand_link || ''}
                                onChange={this._handleNameChange}
                            />
                            {this.state.imagePreviewUrl === '' ? <img src={this.state.brand.image_icon} alt='Brand'/>:$imagePreview}
                            <FieldGroup
                                id="formControlsFile"
                                type="file"
                                label="File"
                                help="Choose brand's image or logo for display"
                                name="image_icon"
                                error={this.state.imageError}
                                onChange={(e)=>this._handleImageChange(e)}
                            />
                            <Button type="submit">
                                {this.props.match === undefined ? 'Submit':'Update'}
                            </Button>
                        </form>
                    </div>
                </Jumbotron>
            </div>
        )
    }
}

AddBrandForm.propTypes = {
    match: PropTypes.object
}

export default AddBrandForm
