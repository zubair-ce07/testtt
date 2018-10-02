import React, {Fragment} from 'react';
import {Grid} from '@material-ui/core/'
import '../App.css';
import {Header, Sidebar} from "./Layout"
import Index from "./Pages/Index"


class App extends React.Component {
    constructor(){
        super();
        this.state = {
            cityId: null,
            cityname: null,
        };
        this.setCity= this.setCity.bind(this)
    }

    setCity(cityId, cityName){
        // console.log("hello: "+cityId)
        this.setState({cityId:cityId, cityName: cityName})
        // debugger;

    }

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
                        <Sidebar setCity={this.setCity} />
                    </Grid>
                    <Grid item sm={10} md={10} className={"actual-body"}>
                        <Index cityId={this.state.cityId} cityName={this.state.cityName} />
                    </Grid>
                </Grid>
                {/*<Grid container>*/}
                    {/*<div>*/}
                        {/*<Footer/>*/}
                    {/*</div>*/}
                {/*</Grid>*/}
            </Fragment>
        );
    }
}

export default App;
