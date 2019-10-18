import React, {Component} from 'react';
import axios from 'axios';


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
        let breadCrumbList = []
        console.log(this.state.product != null)
        breadCrumbList = (this.state.product) ? (
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
                    <div>
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
                var value = [sku.size, sku.out_of_stock]
                if (key in coloursAndSizes) {
                    coloursAndSizes[key] = [...coloursAndSizes[key], value]
                } else {
                    coloursAndSizes[key] =  [value]
                };
            };
        };
        console.log("CCCCCCCCC", coloursAndSizes)
        var skusList = []
        if (coloursAndSizes.length !== 0) {
            console.log("Colours and sizes", coloursAndSizes)
            coloursAndSizes = Object.entries(coloursAndSizes)
            console.log('entries', coloursAndSizes)
            for (var colourAndSizes of coloursAndSizes) {
                skusList.push(<p>Colour: {colourAndSizes[0]}</p>)
                var buttonsList = []
                for (let size of colourAndSizes[1]) {
                    if (size[1]) {
                        buttonsList.push(<label className="btn-floating grey darken-1 center-align"><input type="radio" id={size[0]}/>{size}</label>)
                        // buttonsList.push(<input type="radio" name="gender" value="male"/>)
                    } else {
                        // buttonsList.push(<input type="radio" name="gender" value="male"/>)
                        buttonsList.push(<label className="btn-floating grey darken-3 center-align"><input type="radio" id={size[0]}/>{size}</label>)
                    }
                }
                skusList.push(<div className='row'>{buttonsList}</div>)
            }
        }
        return skusList
    };

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
                            <div className="col s10 offset-s2">{breadCrumbList}</div>
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
                                <label>
        <input name="group1" type="radio" checked />
        <span>Red</span>
      </label>
                                <form>
                                    {skusList}
                                    <label htmlFor="quantity">Quantity: </label>
                                    <input id='quantity' name='quantity' type="number" defaultValue={1} min="1" max="10000"/>
                                </form>
                            </div>
                        </div>

                    </div>
                </div>
            </div>
        )
    };
};

export default Product;
