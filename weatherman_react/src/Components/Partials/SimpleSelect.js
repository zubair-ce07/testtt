import React from "react"
import {withStyles} from '@material-ui/core/styles';
import Input from '@material-ui/core/Input';
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';
import PropTypes from 'prop-types';

const styles = theme => ({
    root: {
        display: 'flex',
        flexWrap: 'wrap',
    },
    formControl: {
        margin: theme.spacing.unit,
        minWidth: 120,
    },
    selectEmpty: {
        marginTop: theme.spacing.unit * 2,
    },
});

class SimpleSelect extends React.Component {
    constructor(props){
        super(props)
        this.state={
            selected: props.selected ? props.selected : "",
        }
    }

    handleSelect(e){
        this.setState({selected: e.target.value})
        this.props.handleSelect(e)
    }

    render() {
        const { classes } = this.props;
        return (
            <form className={classes.root} autoComplete="off">

                <FormControl className={classes.formControl}>
                    <InputLabel htmlFor="simple-select">{this.props.label}</InputLabel>
                    <Select
                        value={this.state.selected}
                        onChange={this.handleSelect.bind(this)}
                        input={<Input name={this.props.label} id="simple-select"/>}
                    >
                        {this.props.items.map((item, index) =>

                        <MenuItem value={item.year} key={index}>{item.year}</MenuItem>
                        )}
                    </Select>
                    {/*<FormHelperText>Some important helper text</FormHelperText>*/}
                </FormControl>
            </form>
        )
    }
}


SimpleSelect.propTypes = {
    classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(SimpleSelect);