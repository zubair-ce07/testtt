import { connect } from 'react-redux';
import React, { Component } from 'react';
import Modal from 'react-responsive-modal';

import { changeModalState } from '../store/actions/modalActions';
import { getPaginationProducts, nextPage, previousPage } from '../store/actions/productActions';
import Pagination from './layout/pagination';
import ProductsList from './products/productlist';
import ProductsFilter from './products/productsfilter';


class Home extends Component {
    componentWillMount = () => {
        const { filters, getPaginationProducts } = this.props;
        getPaginationProducts(1, filters);
    };

    handlePageChange = (buttonId) => {
        const { currentPage, getPaginationProducts,
            nextPage, previousPage, filters } = this.props;
        if (buttonId === 'next') {
            var pageNumber = currentPage + 1;
            nextPage();
        } else if (buttonId === 'previous') {
            var pageNumber = this.props.currentPage - 1;
            previousPage();
        };
        getPaginationProducts(pageNumber, filters);
    };

    handleModalState = () => {
        const { changeModalState } = this.props;
        changeModalState();
    };

    render() {
        const { currentPage } = this.props;
        return (
            <div className="products">
                <br />
                <div className="row">
                    <a className="col s2 offset-s2 btn blue" onClick={this.handleModalState}>
                        Filter Products
                    </a>
                </div>
                <Modal open={this.props.modalOpen} onClose={this.handleModalState} center>
                    <ProductsFilter/>
                </Modal>
                <br />
                <ProductsList />
                <Pagination currentPage={ currentPage } handlePageChange={this.handlePageChange} />
            </div>
        );
    };
};


const mapDispatchToProps = (dispatch) => {
    return {
        getPaginationProducts: (pageNumber, filters) => dispatch(getPaginationProducts(pageNumber, filters)),
        nextPage: () => dispatch(nextPage()),
        previousPage: () => dispatch(previousPage()),
        changeModalState: () => dispatch(changeModalState())
    };
};


const mapStateToProps = (state) => {
    return {
        currentPage: state.product.currentPage,
        modalOpen: state.modal.modalOpen,
        pending: state.product.pending,
        error: state.product.error,
        filters: state.product.filters
    };
};

export default connect(mapStateToProps, mapDispatchToProps)(Home);
