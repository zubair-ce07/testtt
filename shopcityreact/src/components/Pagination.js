import React, { Component } from 'react';


class Pagination extends Component{
    render (){
        const { currentPage, onPageChangeHandler } = this.props;
        return (currentPage !== 1) ? (
            <div className="pagination">
                <ul className="pagination center-align">
                    <li className="waves-effect btn"><a onClick={() => {onPageChangeHandler('previous')}} key='previous'>{'<'}</a></li>
                    <li className="waves-effect btn"><a onClick={() => {onPageChangeHandler('current')}} key='current'>{ currentPage }</a></li>
                    <li className="waves-effect btn"><a onClick={() => {onPageChangeHandler('next')}} key='next'>{'>'}</a></li>
                </ul>
            </div>
        ) : (
            <div className="pagination">
                <ul className="pagination center-align">
                    <li className="waves-effect btn"><a onClick={() => {onPageChangeHandler('current')}} key='current'>{ currentPage }</a></li>
                    <li className="waves-effect btn"><a onClick={() => {onPageChangeHandler('next')}} key='next'>{'>'}</a></li>                    </ul>
            </div>
        )

        }

    };

export default Pagination;
