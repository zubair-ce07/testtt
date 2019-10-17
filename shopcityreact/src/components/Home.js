import React, { Component } from 'react';
import axios from 'axios';
import Modal from 'react-responsive-modal';

import ProductsList from './ProductList';
import Pagination from './Pagination';
import ProductsFilter from './ProductsFilter';


class Home extends Component{
    state = {
        products: [],
        currentPage: 1,
        modalOpen: false,
    }
    componentDidMount = () => {
        axios.get('http://127.0.0.1:8000/api/products/?page=1&Out of Stock=false')
            .then(res => {
                console.log(res)
                this.setState({
                    products: res.data.results
                })
            })
    };
    onPageChangeHandler = (buttonId) => {
        if (buttonId === 'next') {
            let url = 'http://127.0.0.1:8000/api/products/?page='
            let next = this.state.currentPage + 1
            url = url + next + '&Out of Stock=false'
            axios.get(url)
            .then(res => {
                console.log(res)
                this.setState({
                    products: res.data.results,
                    currentPage: this.state.currentPage + 1
                })
            })
        } else if (buttonId === 'previous') {
            let url = 'http://127.0.0.1:8000/api/products/?page='
            let previous = this.state.currentPage - 1
            url = url + previous + '&Out of Stock=false'
            axios.get(url)
            .then(res => {
                console.log(res)
                this.setState({
                    products: res.data.results,
                    currentPage: this.state.currentPage - 1
                })
            })
        };

    };

    onOpenModal = () => {
        this.setState({ modalOpen: true });
      };
     
      onCloseModal = () => {
        this.setState({ modalOpen: false });
      };

    render (){
        const { products } = this.state;
        return (
            <div className="products">
                <br />
                <div className="row">
                    <a className="col s2 offset-s2 btn blue" onClick={this.onOpenModal}>Filter Products</a>
                </div>
                <Modal open={this.state.modalOpen} onClose={this.onCloseModal} center>
                    <ProductsFilter productsList={products} />
                </Modal>
                <br/>
                <ProductsList productsList={products} />
                <Pagination currentPage={this.state.currentPage} onPageChangeHandler={this.onPageChangeHandler}/>
            </div>
        )
    };
};

export default Home;
