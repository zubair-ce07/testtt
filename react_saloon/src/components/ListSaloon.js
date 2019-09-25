import React from 'react';
import ls from 'local-storage';
import PropTypes from 'prop-types';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';
import { fetchSaloons } from '../actions/saloonActions';
import { reactAppConstants } from '../constants/constants';

class ListSaloon extends React.Component {
    cardStyle = {
        margin: '10px',
        width: '100%'
    };

    componentDidMount() {
        this.props.fetchSaloons();
    }

    render() {
        const { saloons } = this.props;
        const saloonsList = saloons.length > 0 ? (
            saloons.map(saloon => saloon.shop_name ? (
                <div className="card" style={this.cardStyle} key={saloon.id}>
                    <div className="card-header">
                        {saloon.shop_name}
                    </div>
                    <div className="card-body">
                        <h5 className="card-title">Phone No : {saloon.phone_no}</h5>
                        <p className="card-text">Address : {saloon.address}</p>
                        {
                            ls.get('token') ? (
                                ls.get(reactAppConstants.USER_TYPE) === reactAppConstants.CUSTOMER ? (<Link to={'/' + saloon.shop_name} className="btn btn-primary" >Reserve a time slot</Link>) : (false)
                            ) : (
                                <Link to="/login" className="btn btn-primary" >Login to Reserve a time slot</Link>
                            )
                        }
                    </div>
                </div >) : (false)
            )
        ) : (
            this.props.successStatus ? (
                <div className="card-header" style={this.cardStyle}>
                        No Saloon To be Listed
                </div>
            ) : (
                <div className="card" style={this.cardStyle}>
                    <div className="card-header" style={this.cardStyle}>
                        Error getting Saloons
                    </div>
                </div>
            )
        );

        return (
            <div className="container">
                {saloonsList}
            </div>

        );
    }
}

ListSaloon.propTypes = {
    saloons: PropTypes.array.isRequired,
    successStatus: PropTypes.bool.isRequired,
    fetchSaloons: PropTypes.func.isRequired
};

const mapStateToPropos = state =>
    (
        {
            saloons: state.saloon.saloons,
            successStatus: state.saloon.successStatus
        }
    );

const mapDispatchToProps = dispatch => 
    (
        {
            fetchSaloons: () =>dispatch(fetchSaloons())
        }
    );

export default connect(mapStateToPropos, mapDispatchToProps)(ListSaloon);