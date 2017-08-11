import React from 'react'
import PropTypes from 'prop-types'
import {Route} from 'react-router-dom'
import {Jumbotron, Button, FormControl,  HelpBlock, FormGroup, ControlLabel} from 'react-bootstrap/lib'

import Navigation from '../Common/Header'
import {createOrUpdateProduct, getOrDeleteProduct} from '../authentication/auth'

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

class AddProductFrom extends React.Component {
    constructor(props){
        super(props)
        this.state = {
            linkError: '',
            nameError: '',
            productIdError: '',
            product: {
                brand: this.props.brand || ''
            }
        }
        this._handleSubmit = this._handleSubmit.bind(this)
        this._handleNameChange = this._handleNameChange.bind(this)
    }

    _handleNameChange(e){
        const product = Object.assign({}, this.state.product)
        product[e.target.name] = e.target.value
        this.setState({
            product
        })
    }

    componentDidMount(){
        if(this.props.match !== undefined){
            getOrDeleteProduct(this.props.match.params.id, 'get', jsonData => {
                console.log(jsonData)
                let product = Object.assign({}, jsonData)
                this.setState({
                    product,
                })
            })
        }
    }
    validateURL(textval) {
        const urlregex = /^(https?|ftp):\/\/([a-zA-Z0-9.-]+(:[a-zA-Z0-9.&%$-]+)*@)*((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9][0-9]?)(\.(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])){3}|([a-zA-Z0-9-]+\.)*[a-zA-Z0-9-]+\.(com|edu|gov|int|mil|net|org|biz|arpa|info|name|pro|aero|coop|museum|[a-zA-Z]{2}))(:[0-9]+)*(\/($|[a-zA-Z0-9.,?'\\+&%$#=~_-]+))*$/;
        return urlregex.test(textval);
    }
    _handleSubmit(e){
        e.preventDefault()
        let bool = false
        let nameError, productIdError
        let linkError = nameError = productIdError = ''
        if(e.target.formControlsProductID.value.length === 0){
            productIdError = 'Id of the product is required'
            document.getElementById('formControlsProductID').focus()
            bool = true
        }
        if(e.target.formControlsProductName.value.length === 0){
            nameError = 'Name is required!'
            if(!bool){
                document.getElementById('formControlsProductName').focus()
            }
            bool = true
        }
        if(!this.validateURL(e.target.formControlsProductSource.value.toString())){
            linkError = 'Invalid URL'
            if(!bool){
                document.getElementById('formControlsProductSource').focus()
            }
            bool = true
        }
        this.setState({
                linkError,
                nameError,
                productIdError
        })
        if(bool){
            return false
        }
        let data = document.getElementById('productCreate')

        if(this.props.match === undefined){
            createOrUpdateProduct(data, false, jsonData => {
                data.reset()
                this.setState({
                    linkError: '',
                    nameError: '',
                    productIdError: '',
                    product: {},
                })
                toastr.success('product created successfully!')
            })
        }
        else{
            createOrUpdateProduct(data, true, jsonData => {
                this.setState({
                    linkError: '',
                    nameError: '',
                    productIdError: '',
                    product: jsonData,
                })
                toastr.success('product created successfully!')
            })
        }
        // if(this.props.match === undefined){
        //     createOrUpdateProduct(data, false, (jsonData) => {
        //         data.reset()
        //         this.setState({
        //             file: '',
        //             imagePreviewUrl: '',
        //             binaryString: '',
        //             linkError: '',
        //             nameError: '',
        //             imageError: '',
        //             product: {}
        //         })
        //         toastr.success('product created successfully!')
        //     })
        // }
        // else{
        //     createOrUpdateProduct(data, true, (jsonData) => {
        //         this.setState({
        //             file: '',
        //             imagePreviewUrl: '',
        //             binaryString: '',
        //             linkError: '',
        //             nameError: '',
        //             imageError: '',
        //             product: jsonData
        //         })
        //         toastr.success('product updated successfully!')
        //     })
        // }
    }
    render(){
        return (
            <div>
                {this.props.match !== undefined ? <Route component={Navigation} />:''}
                <Jumbotron>
                    <div className='container'>
                        <h1>{this.props.match === undefined ? 'Add A New Product!!':'Update This Product!!'}</h1>
                        <form id="productCreate" onSubmit={this._handleSubmit}>
                            <input type="hidden" value={this.props.match ? this.props.match.params.id:''} name='pk'/>
                            <input type="hidden" value={this.state.product.brand ? this.state.product.brand:''} name='name'/>
                            <FieldGroup
                                id="formControlsProductID"
                                type="text"
                                label="Product's ID"
                                placeholder="Enter product identification string"
                                name="product_id"
                                error={this.state.productIdError}
                                value={this.state.product.product_id || ''}
                                onChange={this._handleNameChange}
                            />
                            <FieldGroup
                                id="formControlsProductName"
                                type="text"
                                label="Product Name"
                                placeholder="Enter product name"
                                name="product_name"
                                error={this.state.nameError}
                                value={this.state.product.product_name || ''}
                                onChange={this._handleNameChange}
                            />
                            <FieldGroup
                                id="formControlsProductSource"
                                type="text"
                                label="Product Page's Link"
                                placeholder="Enter product source Link"
                                name="source_url"
                                error={this.state.linkError}
                                value={this.state.product.source_url || ''}
                                onChange={this._handleNameChange}
                            />
                            <FieldGroup
                                id="formControlsProductCategory"
                                type="text"
                                label="Product's Category"
                                placeholder="Enter product category"
                                name="category"
                                value={this.state.product.category || ''}
                                onChange={this._handleNameChange}
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

AddProductFrom.propTypes = {
    match: PropTypes.object,
    brand: PropTypes.string
}

export default AddProductFrom
