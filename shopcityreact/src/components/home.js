import React, { Component } from 'react';
import axios from 'axios';
import Modal from 'react-responsive-modal';
import { connect } from 'react-redux';

import { getPaginationProducts, nextPage, previousPage } from '../store/actions/productActions';
import { changeModalState } from '../store/actions/modalActions';
import ProductsList from './products/productlist';
import Pagination from './layout/pagination';
import ProductsFilter from './products/productsfilter';


class Home extends Component {
    componentDidMount = () => {
        this.props.getPaginationProducts(1)
    };
    onPageChangeHandler = (buttonId) => {
        if (buttonId === 'next') {
            let next = this.props.currentPage + 1
            this.props.getPaginationProducts(next)
            this.props.nextPage()
        } else if (buttonId === 'previous') {
            let previous = this.props.currentPage - 1
            this.props.getPaginationProducts(previous)
            this.props.previousPage()
        };
    };

    modalHandler = () => {
        this.props.changeModalState();
    };

    render() {
        console.log("THESE ARE PROPS: ", this.props)
        const products = (this.props.products) ? (this.props.products) : ([]);
        return (
            <div className="products">
                <br />
                <div className="row">
                    <a className="col s2 offset-s2 btn blue" onClick={this.modalHandler}>Filter Products</a>
                </div>
                <Modal open={this.props.modalOpen} onClose={this.modalHandler} center>
                    {/* <ProductsFilter productsList={products} /> */}
                    <ProductsList productsList={products} />
                </Modal>
                <br />
                <ProductsList productsList={products} />
                <Pagination currentPage={this.props.currentPage} onPageChangeHandler={this.onPageChangeHandler} />
            </div>
        )
    };
};

const mapDispatchToProps = (dispatch) => {
    return {
        getPaginationProducts: (pageNumber) => dispatch(getPaginationProducts(pageNumber)),
        nextPage: () => dispatch(nextPage()),
        previousPage: () => dispatch(previousPage()),
        changeModalState: () => dispatch(changeModalState())
    }
};

const mapStateToProps = (state) => {
    return {
        products: state.product.products,
        currentPage: state.product.currentPage,
        modalOpen: state.modal.modalOpen
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(Home);
