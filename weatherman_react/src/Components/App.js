import React, {Fragment} from 'react';
import {Grid} from '@material-ui/core/'
import '../App.css';
import {Header, Sidebar} from "./Layout"


class App extends React.Component {

    render() {
        return (
            <Fragment>
                <Grid container>
                    <Grid item sm md lg>
                        <Header/>
                    </Grid>
                </Grid>
                <Grid container>
                    <Grid item xs={12} sm={2} md={2}>
                        <Sidebar/>
                    </Grid>
                    <Grid item sm={10} md={10} className={"actual-body"}>
                        {this.props.children}
                    </Grid>
                </Grid>

            </Fragment>
        );
    }
}

export default App;
