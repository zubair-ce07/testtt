import { connect } from 'react-redux';
import React, {Component} from 'react';

import { addToCart } from '../../store/actions/authActions';
import { getProductDetail } from '../../store/actions/productActions';
import { setOutOfStock } from '../../store/actions/productActions';


class Product extends Component {
    state = {
        productId: this.props.match.params.product_id,
        skuId: null,
        quantity: 1
    };

    componentWillMount () {
        let productId = this.props.match.params.product_id;
        this.props.getProductDetail(productId);
    };

    handleChange = (e) => {
        e.persist();
        this.setState({
            [e.target.id]: e.target.value
        });
    };

    handleSubmit = (e) => {
        const { user, addToCart, setOutOfStock } = this.props;
        e.preventDefault();
        if (user.isSuperUser) {
            setOutOfStock(this.state);
        } else if (user.isAuthenticated) {
            addToCart(this.state);
        } else {
            this.props.history.push('/login');
        };
    };

    renderBreadCrumb = (product) => {
        let breadCrumbList = (product) ? (
            product.categories.slice(0,3).map(category => {
                return (
                    <a href="#" key={category.category}>
                        {category.category}/
                    </a>
                )
            })
        ) : (
            <p>Loading...</p>
        )
        return breadCrumbList;
    };

    renderImages = (product) => {
        let imagesList = (product) ? (
            product.image_url.split(';').map(image => {
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

    renderProductTitle = (product) => {
        var productTitle = (product) ? (
            product.name + '-' + product.brand
        ):("Loading...")
        return productTitle;
    };

    renderProductPrice = (product) => {
        var productPrice = (product) ? (
            product.price + '-' + product.currency
        ) : ('Loading...')
        return productPrice;
    };

    renderMainImage = (product) => {
        var mainImage = (product) ? (product.image_url) : '';
        mainImage = mainImage ? (mainImage.split(';')[0]) : '';
        mainImage = mainImage ? (mainImage.replace('medium', 'large')) : '';
        return mainImage;
    };

    getColourAndSizes = (product) => {
        var coloursAndSizes = {};
        var skus = (product) ? (
            product.skus
        ) : (
            'Loading...'
        );
        if (product) {
            for (var sku of skus) {
                var key = sku.colour;
                var value = {size: sku.size, out_of_stock: sku.out_of_stock};
                (key in coloursAndSizes) ? (
                    coloursAndSizes[key] = [...coloursAndSizes[key], value]
                ) : (
                    coloursAndSizes[key] =  [value]
                )
            };
        };
        return coloursAndSizes;
    };

    renderSkus = (product) => {
        var coloursAndSizes = this.getColourAndSizes(product);
        var skusList = []

        if (coloursAndSizes.length !== 0) {
            coloursAndSizes = Object.entries(coloursAndSizes);
            for (var colourAndSizes of coloursAndSizes) {
                skusList.push(<p key={colourAndSizes}>Colour: {colourAndSizes[0]}</p>);
                var buttonsList = [];
                for (let size of colourAndSizes[1]) {
                    (size.out_of_stock) ? (
                        buttonsList.push(
                            <label key={size.size} className="btn grey lighten-1 center-align">
                                <input onChange={ this.handleChange } id='skuId' name="group1" type="radio" disabled/>
                                <span>{size.size}</span>
                            </label>
                        )
                     ) : (
                        buttonsList.push(
                            <label key={size.size} className="btn grey darken-3 center-align">
                                <input onChange={ this.handleChange } id='skuId' value={colourAndSizes[0] + '_' + size.size} name="group1" type="radio"/>
                                <span>{size.size}</span>
                            </label>
                        )
                     )
                };
                skusList.push(
                    <div key={Math.random()} className='row'>
                        {buttonsList}
                    </div>
                );
            };
        };
        return skusList;
    };

    addToCartOrSetOutOfStock = () => {
        const { user } = this.props;
        let addToCartOrOutOfStockButton = (user.isSuperUser) ? (
                <div>
                    <div className="input-field center-align">
                        <button type='submit' className="btn waves-effect waves-light">
                            Set Out of Stock
                        </button>
                    </div>
                </div>
         ) : (
                <div>
                    <label htmlFor="quantity">Quantity: </label>
                    <input onChange={this.handleChange} id='quantity' name='quantity' type="number" defaultValue={1} min="1" max="10000"/>
                    <div className="input-field center-align">
                        <button type='submit' className="btn waves-effect waves-light">
                            Add To Cart
                        </button>
                    </div>
                </div>
        )
        return addToCartOrOutOfStockButton;
    };

    render () {
        const { product } = this.props;
        let breadCrumbList = this.renderBreadCrumb(product);
        let imagesList = this.renderImages(product);
        let productTitle = this.renderProductTitle(product);
        let productPrice = this.renderProductPrice(product);
        let mainImage = this.renderMainImage(product);
        let skusList = this.renderSkus(product);
        let addToCartOrSetOutOfStock = this.addToCartOrSetOutOfStock();
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
                                <form onSubmit={this.handleSubmit} className="white">
                                    { skusList }
                                    { addToCartOrSetOutOfStock }
                                </form>
                            </div>
                        </div>

                    </div>
                </div>
            </div>
        );
    };
};


const mapDispatchToProps = (dispatch) => {
    return {
        getProductDetail: (productId) => dispatch(getProductDetail(productId)),
        addToCart: (cartItem) => dispatch(addToCart(cartItem)),
        setOutOfStock: (productDetails) => dispatch(setOutOfStock(productDetails))
    };
};


const mapStateToProps = (state) => {
    return {
        user: state.auth.user,
        product: state.product.product
    };
};

export default connect(mapStateToProps, mapDispatchToProps)(Product);
