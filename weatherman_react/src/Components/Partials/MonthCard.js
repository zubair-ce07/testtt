import React from 'react';
import PropTypes from 'prop-types';
import {withStyles} from '@material-ui/core/styles';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import Typography from '@material-ui/core/Typography';
import {monthNames} from "../../constants";

const styles = {
    card: {
        minWidth: 275,
    },
    bullet: {
        display: 'inline-block',
        margin: '0 2px',
        transform: 'scale(0.8)',
    },
    title: {
        marginBottom: 16,
        fontSize: 14,
    },
    pos: {
        marginBottom: 12,
    },
};

function MonthCard(props) {
    const {classes} = props;
    const monthName = monthNames[props.month.month]
    return (
        <Card className={classes.card}>
            <CardContent>
                <Typography variant="headline" component="h2">
                    Weather Report of {monthName}
                </Typography>
                <Typography component="h3">
                    Average Highest Temperature: <span>{props.month.higest_average}&deg;C</span>
                    <br/>
                    Average Lowest Temperature: <span>{props.month.lowest_average}&deg;C</span>
                    <br/>
                    Average Humidity: <span>{props.month.average_humidity}%</span>
                    <br/>
                </Typography>
            </CardContent>
        </Card>
    );
}

MonthCard.propTypes = {
    classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(MonthCard);