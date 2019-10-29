import React from 'react';


const Pagination = (props) => {
    const { currentPage, handlePageChange } = props;

    return (currentPage !== 1) ? (
        <div className="pagination">
            <ul className="pagination center-align">
                <li className="waves-effect btn">
                    <a onClick={() => {handlePageChange('previous')}} key='previous'>
                        {'<'}
                    </a>
                </li>
                <li className="waves-effect btn">
                    <a onClick={() => {handlePageChange('current')}} key='current'>
                        { currentPage }
                    </a>
                </li>
                <li className="waves-effect btn">
                    <a onClick={() => {handlePageChange('next')}} key='next'>
                        {'>'}
                    </a>
                </li>
            </ul>
        </div>
    ) : (
        <div className="pagination">
            <ul className="pagination center-align">
                <li className="waves-effect btn">
                    <a onClick={() => {handlePageChange('current')}} key='current'>
                        { currentPage }
                    </a>
                </li>
                <li className="waves-effect btn">
                    <a onClick={() => {handlePageChange('next')}} key='next'>
                        {'>'}
                    </a>
                </li>
            </ul>
        </div>
    )
};

export default Pagination;
