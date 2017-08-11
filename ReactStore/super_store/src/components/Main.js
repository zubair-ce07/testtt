import React from 'react'
import {Route} from 'react-router-dom'

import App from './App'
import Login from './LogInOut/Login'
import SelectedBrand from './SelectedBrand'
import ItemDetail from './ItemDetail/ItemDetail'
import AddBrandForm from './Forms/AddBrandForm'
import AddProductForm from './Forms/AddProductForm'

const MainApp = (props) => {
    return (
        <div>
            <Route
                path="/app/login/"
                component={Login}
            />
            <Route
                path="/home/:name"
                component={App}
            />
            <Route
                exact
                path='/brand/:name'
                component={SelectedBrand}
            />
            <Route
                path='/product/:id([0-9]+)(-[\s\S]*)'
                component={ItemDetail}
            />
            <Route
                path='/brand/update/:id'
                component={AddBrandForm}
            />
            <Route
                path='/product/update/:id'
                component={AddProductForm}
            />
        </div>
    )
}

export default MainApp
