/**
 * Created by mzulqarnain on 1/30/18.
 */
import React, {Component} from 'react';
import PropTypes from 'prop-types';
import {withStyles} from 'material-ui/styles';
import Table, {TableBody, TableCell, TableHead, TableRow} from 'material-ui/Table';
import Paper from 'material-ui/Paper';

const styles = theme => ({
    root: {
        width: '100%',
        marginTop: theme.spacing.unit * 3,
        overflowX: 'auto',
    },
    Table: {
        minWidth: 700,
    },
});

class ResultList extends Component {

    render() {
        return (
            <Paper>
                <Table>
                    <TableHead cellSpacing={100}>
                        <TableRow>
                            <th>Temperature (Kelvin)</th>
                            <th>Pressure (hPa)</th>
                            <th>Humidity (%)</th>
                            <th>Clouds (%)</th>
                            <th>Wind Speed (Meter/Sec)</th>
                        </TableRow>
                    </TableHead>

                    <TableBody>
                        {this.props.data.map(this.renderTable)}
                    </TableBody>

                </Table>
            </Paper>
        );//return
    }//render

    renderTable(data) {

        return (
            <TableRow>
                <TableCell>{data.main.temp}</TableCell>
                <TableCell>{data.main.pressure}</TableCell>
                <TableCell>{data.main.humidity}</TableCell>
                <TableCell>{data.clouds.all}</TableCell>
                <TableCell>{data.wind.speed}</TableCell>
            </TableRow>
        );
    }
}//class

export default withStyles(styles)(ResultList);