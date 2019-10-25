import React, {Component} from 'react';
import axios from 'axios';

import { connect } from 'react-redux';


class Product extends Component {
    state = {
        product_id: null,
        product: null
    }
    componentDidMount () {
        let product_id = this.props.match.params.product_id;
        axios.get('http://127.0.0.1:8000/api/products/' + product_id + '/')
        .then(res => {
            console.log(res)
            this.setState({
                product: res.data,
                product_id: product_id
            })
        })
    }

    breadCrumb = () => {
        console.log(this.state.product != null)
        let breadCrumbList = (this.state.product) ? (
            this.state.product.categories.slice(0,3).map(category => {
                return (
                    <a href="#" key={category.category}>{category.category}/</a>
                )
            })
        ) : (
            <p>Loading...</p>
        )
        return breadCrumbList
    };

    images = () => {
        let imagesList = []
        imagesList = (this.state.product) ? (
            this.state.product.image_url.split(';').map(image => {
                return (
                    <div key={Math.random()}>
                        <img style={{height: '250px'}} src={image}></img><br/>
                    </div>
                )
            })
        ) : (
            <p>Loading...</p>
        )
        return imagesList;
    };

    productTitle = () => {
        var productTitle = (this.state.product) ? (
            this.state.product.name + '-' + this.state.product.brand
        ):("Loading...")
        return productTitle;
    };

    productPrice = () => {
        var productPrice = (this.state.product) ? (
            this.state.product.price + '-' + this.state.product.currency
        ) : ('Loading...')
        return productPrice;
    };

    mainImage = () => {
        var mainImage = (this.state.product) ? (this.state.product.image_url) : ''
        mainImage = mainImage ? (mainImage.split(';')[0]) : ''
        mainImage = mainImage ? (mainImage.replace('medium', 'large')) : ''
        return mainImage
    }

    skus = () => {
        var coloursAndSizes = {}
        var skus = (this.state.product) ? (
            this.state.product.skus
        ) : (
            'Loading...'
        )
        if (this.state.product) {
            for (var sku of skus) {
                var key = sku.colour
                var value = {size: sku.size, out_of_stock: sku.out_of_stock}
                if (key in coloursAndSizes) {
                    coloursAndSizes[key] = [...coloursAndSizes[key], value]
                } else {
                    coloursAndSizes[key] =  [value]
                };
            };
        };
        var skusList = []
        if (coloursAndSizes.length !== 0) {
            console.log("Colours and sizes", coloursAndSizes)
            coloursAndSizes = Object.entries(coloursAndSizes)
            console.log('entries', coloursAndSizes)
            for (var colourAndSizes of coloursAndSizes) {
                skusList.push(<p key={colourAndSizes}>Colour: {colourAndSizes[0]}</p>)
                var buttonsList = []
                for (let size of colourAndSizes[1]) {
                    console.log(size)
                    if (size.out_of_stock) {
                        buttonsList.push(<label key={size.size} className="btn grey lighten-1 center-align" id={size.size}><input name="group1" type="radio" id={size.size} disabled/><span>{size.size}</span></label>)
                    } else {
                        buttonsList.push(<label key={size.size} className="btn grey darken-3 center-align"><input value={colourAndSizes[0] + '_' + size.size} name="group1" type="radio" id='sku'/><span>{size.size}</span></label>)
                    }
                }
                skusList.push(<div key={Math.random()} className='row'>{buttonsList}</div>)
            }
        }
        return skusList
    };

    addToCart = (e) => {
        e.preventDefault()
        console.log('submitted');
        console.log(document.getElementById('quantity').value);
        console.log(document.getElementById('sku').value);
    }

    render () {
        let breadCrumbList = this.breadCrumb()
        let imagesList = this.images()
        let productTitle = this.productTitle()
        let productPrice = this.productPrice()
        let mainImage = this.mainImage()
        let skusList = this.skus()
        return (
            <div className="product-details">
                <div className="row">
                    <div className="col s4">
                        <div className='row'>
                            <br/>
                            <div className="col s10 offset-s2">
                                <a href="/" key="home">Home/</a>
                                {breadCrumbList}
                            </div>
                        </div>
                        <div className="row">
                            <div className="col s10 offset-s2">{imagesList}</div>
                        </div>
                    </div>
                    <div className="col s3">
                        <div className="row">
                            <br/>
                            <img className="col s12" src={mainImage} alt=""/>
                        </div>

                    </div>
                    <div className="col s5">
                        <div className="row">
                            <div className="col s8 offset-4">
                                <br/>
                                <h5>{productTitle}</h5>
                                <h6>Price: {productPrice}</h6>
                                <form>
                                    {skusList}
                                    <label htmlFor="quantity">Quantity: </label>
                                    <input id='quantity' name='quantity' type="number" defaultValue={1} min="1" max="10000"/>
                                    <div className="input-field center-align">
                                        <button className="btn waves-effect waves-light" type="submit" name="action" onClick={this.addToCart}>Add To Cart</button>
                                    </div>
                                </form>
                            </div>
                        </div>

                    </div>
                </div>
            </div>
        )
    };
};

const mapDispatchToProps = (dispatch) => {
    return {
    }
};

const mapStateToProps = (state) => {
    return {
        user: state.auth.user,
        registerPending: state.auth.registerPending,
        registerError: state.auth.registerError
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(Product);
