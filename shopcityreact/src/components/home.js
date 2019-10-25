import React, { Component } from 'react';
import Modal from 'react-responsive-modal';
import { connect } from 'react-redux';

import { getPaginationProducts, nextPage, previousPage } from '../store/actions/productActions';
import { changeModalState } from '../store/actions/modalActions';
import ProductsList from './products/productlist';
import Pagination from './layout/pagination';
import ProductsFilter from './products/productsfilter';


class Home extends Component {
    componentWillMount = () => {
        const { filters, getPaginationProducts } = this.props;
        getPaginationProducts(1, filters);
    };
    onPageChangeHandler = (buttonId) => {
        if (buttonId === 'next') {
            let next = this.props.currentPage + 1
            const { filters } = this.props;
            this.props.getPaginationProducts(next, filters)
            this.props.nextPage()
        } else if (buttonId === 'previous') {
            let previous = this.props.currentPage - 1
            const { filters } = this.props;
            this.props.getPaginationProducts(previous, filters)
            this.props.previousPage()
        };
    };

    modalHandler = () => {
        this.props.changeModalState();
    };

    render() {
        return (
            <div className="products">
                <br />
                <div className="row">
                    <a className="col s2 offset-s2 btn blue" onClick={this.modalHandler}>Filter Products</a>
                </div>
                <Modal open={this.props.modalOpen} onClose={this.modalHandler} center>
                    <ProductsFilter/>
                </Modal>
                <br />
                <ProductsList />
                <Pagination currentPage={this.props.currentPage} onPageChangeHandler={this.onPageChangeHandler} />
            </div>
        )
    };
};

const mapDispatchToProps = (dispatch) => {
    return {
        getPaginationProducts: (pageNumber, filters) => dispatch(getPaginationProducts(pageNumber, filters)),
        nextPage: () => dispatch(nextPage()),
        previousPage: () => dispatch(previousPage()),
        changeModalState: () => dispatch(changeModalState())
    }
};

const mapStateToProps = (state) => {
    return {
        currentPage: state.product.currentPage,
        modalOpen: state.modal.modalOpen,
        pending: state.product.pending,
        error: state.product.error,
        filters: state.product.filters
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(Home);
