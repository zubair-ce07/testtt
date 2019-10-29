import { connect } from 'react-redux';
import React, { Component } from 'react';

import { setOptions, changeModalState } from '../../store/actions/modalActions';
import { getPaginationProducts, resetPage } from '../../store/actions/productActions';


class ProductsFilter extends Component{
    state = {
        brand: '',
        size: '',
        colour: '',
        category: '',
        minimum: '',
        maximum: '',
        name: '',
        outOfStock: false
    };

    componentWillMount = () => {
        const { setOptions } = this.props;
        setOptions();
    };

    handleChange = (e) => {
        e.persist();
        this.setState({
            [e.target.id]: e.target.value
        });
    };

    handleSearch = (e) => {
        e.preventDefault();
        const { getPaginationProducts, resetPage, currentPage, changeModalState } = this.props;
        resetPage();
        getPaginationProducts(currentPage, this.state);
        changeModalState();
    };

    renderBrandOptions = () => {
        const { brandChoices } = this.props;
        const brandOptions = (brandChoices !== null) ? (
            brandChoices.map(brand => {
                return (
                    <option key={brand}>{brand}</option>
                )
            }
        )
        ) : (
            <option>Nothing</option>
        );
        return brandOptions;
    };

    renderSizeOptions = () => {
        const { sizeChoices } = this.props;
        const sizeOptions = (sizeChoices !== null) ? (
            sizeChoices.map(size => {
                return (
                    <option key={size}>{size}</option>
                )
            })
        ) : (
            <option>Nothing</option>
        );
        return sizeOptions;
    };

    renderColourOptions = () => {
        const { colourChoices } = this.props;
        const colourOptions = (colourChoices !== null) ? (
            colourChoices.map(colour => {
                return (
                    <option key={colour}>{colour}</option>
                )
            })
        ) : (
            <option>Nothing</option>
        );
        return colourOptions;
    };

    renderCategoryOptions = () => {
        const { categoryChoices } = this.props;
        const categoryOptions = (categoryChoices !== null) ? (
            categoryChoices.map(category => {
                return (
                    <option key={category}>{category}</option>
                )
            })
        ) : (
            <option>Nothing</option>
        );
        return categoryOptions;
    };

    render (){
        const { optionsPending, optionsError } = this.props;
        const brands = this.renderBrandOptions();
        const sizes = this.renderSizeOptions();
        const colours = this.renderColourOptions();
        const categories = this.renderCategoryOptions();

        if (optionsPending) {
            return (
                <div>Loading...</div>
            );
        } else if (optionsError !== null) {
            return (
                <div>{optionsError}</div>
            );
        };

        return (
            <div>
                <form onSubmit={this.handleSearch}>
                <div className="row">
                    <div className="input-field col s12">
                        <input id="name" type="text" className="validate" onChange={this.handleChange}/>
                        <label htmlFor="name">Name</label>
                    </div>
                </div>
                <div className="row">
                    <div className="input-field col s6">
                        <input id="minimum" type="number" className="validate" min="0" max="10000" onChange={this.handleChange}/>
                        <label htmlFor="minimum">Minimum</label>
                    </div>
                    <div className="input-field col s6">
                        <input id="maximum" type="number" className="validate" min="0" max="10000" onChange={this.handleChange}/>
                        <label htmlFor="maximum">Maximum</label>
                    </div>
                </div>
                <div className="row">
                    Brand:&nbsp;
                    <div className="input-field col s12">
                    <select name='brand' id='brand' className="browser-default" onClick={this.handleChange}>
                        <option key='default' value=""></option>
                        {brands}
                    </select>
                    </div>
                </div>
                <div className="row">
                    Size:&nbsp;
                    <div className="input-field col s12">
                    <select name='size' id='size' className="browser-default" onClick={this.handleChange}>
                        <option key='default' value=""></option>
                        {sizes}
                    </select>
                    </div>
                </div>
                <div className="row">
                    Colour:&nbsp;
                    <div className="input-field col s12">
                    <select name='colour' id='colour' className="browser-default" onClick={this.handleChange}>
                        <option key='default' value=""></option>
                        {colours}
                    </select>
                    </div>
                </div>
                <div className="row">
                    Category:&nbsp;
                    <div className="input-field col s12">
                    <select name='category' id='category' className="browser-default" onClick={this.handleChange}>
                        <option key='default' value=""></option>
                        {categories}
                    </select>
                    </div>
                </div>
                <div className="row">
                    Out Of Stock:&nbsp;
                    <div className="input-field col s12">
                    <select name='outOfStock' id='outOfStock' className="browser-default" onClick={this.handleChange}>
                        <option key='false' value="false">No</option>
                        <option key='true' value="true">Yes</option>
                    </select>
                    </div>
                </div>
                <div className="input-field center-align">
                    <button className="btn waves-effect waves-light" type="submit" name="action">Search</button>
                </div>
                </form>
            </div>
        );
    };
};


const mapDispatchToProps = (dispatch) => {
    return {
        setOptions: () => dispatch(setOptions()),
        getPaginationProducts: (currentPage, filters) => dispatch(getPaginationProducts(currentPage, filters)),
        resetPage: () => dispatch(resetPage()),
        changeModalState: () => dispatch(changeModalState())
    };
};

const mapStateToProps = (state) => {
    return {
        brandChoices: state.modal.options.brandChoices,
        sizeChoices: state.modal.options.sizeChoices,
        colourChoices: state.modal.options.colourChoices,
        categoryChoices: state.modal.options.categoryChoices,
        optionsPending: state.modal.optionsPending,
        optionsError: state.modal.optionsError,
        currentPage: state.product.currentPage
    };
};

export default connect(mapStateToProps, mapDispatchToProps)(ProductsFilter);
