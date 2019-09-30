import localStorage from 'local-storage';
import React from 'react';
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
import Container from '@material-ui/core/Container';
import withStyles from '@material-ui/styles/withStyles';
import { appStyles } from '../styles/appStyles';

class ListSaloon extends React.Component {

    componentDidMount() {
        this.props.fetchSaloons();
    }
    render() {
        const { classes } = this.props;
        const { saloons } = this.props;
        const saloonsList = saloons.length > 0 ? (
            saloons.map(saloon => saloon.shop_name ? (
                <Card className={classes.cardStyle} key={saloon.id}>
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
                            localStorage.get('token') ? (
                                localStorage.get(reactAppConstants.USER_TYPE) === reactAppConstants.CUSTOMER ? (
                                    <Button size="small" variant="contained" color="primary">
                                        <Link to={routeConstants.LIST_SALOONS_ROUTE+ saloon.shop_name}
                                            className={classes.navBarLink}>
                                            Reserve a time slot
                                        </Link>
                                    </Button>) : (false)
                            ) : (
                                <Button size="small" variant="contained" color="primary">
                                    <Link to={routeConstants.LOGIN_ROUTE}
                                        className={classes.navBarLink}>
                                        Login to Reserve a time slot
                                    </Link>
                                </Button>
                            )
                        }
                    </CardActions>
                </Card>

            ) : (false)
            )
        ) : (
            this.props.successStatus ? (
                <Card className={classes.cardStyle}>
                    <CardContent>
                        <Typography gutterBottom variant="h5" component="h2">
                            No Saloons To be Listed
                        </Typography>
                    </CardContent>
                </Card>
            ) : (
                <Card className={classes.cardStyle}>
                    <CardContent>
                        <Typography gutterBottom variant="h5" component="h2">
                            Errors Getting Saloons List
                        </Typography>
                    </CardContent>
                </Card>
            )
        );
        return (
            <Container>
                {saloonsList}
            </Container>
        );
    }
}

ListSaloon.propTypes = {
    saloons: PropTypes.array.isRequired,
    successStatus: PropTypes.bool.isRequired,
    fetchSaloons: PropTypes.func.isRequired,
    classes: PropTypes.object.isRequired
};

const mapStateToProps = state =>({
    saloons: state.saloon.saloons,
    successStatus: state.saloon.successStatus
});

const mapDispatchToProps = dispatch => ({
    fetchSaloons: () => dispatch(fetchSaloons())
});

//multiple hoc without compose
export default (connect(mapStateToProps, mapDispatchToProps))(withStyles(appStyles)(ListSaloon));