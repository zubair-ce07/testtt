import React from 'react';
import ls from 'local-storage';
import PropTypes from 'prop-types';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';
import { fetchSaloons } from '../actions/saloonActions';
import { reactAppConstants } from '../constants/constants';
import { routeConstants } from '../constants/routeConstants';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import CardActions from '@material-ui/core/CardActions';

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
                <Card style={this.cardStyle} key={saloon.id}>
                    <CardContent>
                        <Typography gutterBottom variant="h5" component="h2">
                            {saloon.shop_name}
                        </Typography>
                        <Typography variant="h6" component="h2">
                            Phone No : {saloon.phone_no}
                        </Typography>
                        <Typography variant="h6" component="h2">
                            Address : {saloon.address}
                        </Typography>
                    </CardContent>
                    <CardActions>
                        {
                            ls.get('token') ? (
                                ls.get(reactAppConstants.USER_TYPE) === reactAppConstants.CUSTOMER ? (
                                    <Button size="small" color="primary">
                                        <Link to={routeConstants.LIST_SALOONS_ROUTE+ saloon.shop_name} >Reserve a time slot</Link>
                                    </Button>) : (false)
                            ) : (
                                <Button size="small" color="primary">
                                    <Link to={routeConstants.LOGIN_ROUTE} >Login to Reserve a time slot</Link>
                                </Button>
                            )
                        }
                    </CardActions>
                </Card>

            ) : (false)
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