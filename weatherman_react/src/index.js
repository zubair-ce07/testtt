import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter as Router, Route, Switch, Redirect } from 'react-router-dom'
import './index.css';
import App from './Components/App';
import registerServiceWorker from './registerServiceWorker';

import Index from './Components/Pages/Index'
import Detail from './Components/Pages/Detail'
import NotFound from './Components/Pages/NotFound'

ReactDOM.render(
    <Router>
        <App exact path="/">
            <Switch>
                <Route exact path="/" component={Index}/>
                <Redirect from="/index" to="/" />
                <Route path="/city/:cityId/:cityName" component={Detail}/>
                {/*For 404 page*/}
                <Route render={(props) => <NotFound {...props} notFound={true} /> }/>
            </Switch>
        </App>

    </Router>,
    document.getElementById('root'));
registerServiceWorker();