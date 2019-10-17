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
        if (this.state.product) {
            for (let category of this.state.product.categories.slice(0,3)) {
                breadCrumbList.push(<a href="#">{category.category}/</a>)
            }
            breadCrumbList.push(<a href="#">{this.state.product_id}/</a>)
        } else {
            breadCrumbList.push(<p>No categories</p>)
        }
        return breadCrumbList
    };

    images = () => {
        let imagesList = []
        if (this.state.product) {
            let imageUrls = this.state.product.image_url.split(';')
            for (let image of imageUrls) {
                imagesList.push(
                    <div>
                        <img alt="" style={{height: '250px'}} src={image}></img><br/>
                    </div>
                )
            }
        } else {
            imagesList.push(<p>No Images</p>)
        };
        return imagesList;
    };

    productTitle = () => {
        var productTitle = ''
        if (this.state.product) {
            productTitle = this.state.product.name + '-' + this.state.product.brand
        } else {
            productTitle = "No Title"
        };
        return productTitle;
    };

    render () {
        let breadCrumbList = this.breadCrumb()
        let imagesList = this.images()
        let productTitle = this.productTitle()
        var mainImage = ''
        if (this.state.product) {
            mainImage = this.state.product.image_url
        }
        return (
            <div className="product-details">
                <div className="row">
                    <div className="col s4">
                        <div className='row'>
                            <div className="col s2"></div>
                            <br/>
                            <div className="col s10">{breadCrumbList}</div>
                        </div>
                        <div className="row">
                            <div className="col s2"></div>
                            <div className="col s10">{imagesList}</div>
                        </div>
                    </div>
                    <div className="col s4">
                        <br/>
                        <img src={mainImage} alt="" height='500'/>
                    </div>
                    <div className="col s4">
                        <br/>
                        <h4>{productTitle}</h4>
                    </div>
                </div>
            </div>
        )
    };
};

export default Product;
