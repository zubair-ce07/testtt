import React from 'react'
import ProtectedRoute from './protected.route'
import UserRoute from './user.route'
import LoginPage from '../pages/login'
import RegisterPage from '../pages/register'
import HomePage from '../pages/home'
// import AboutUs from '../pages/aboutus'
// import CheckoutPage from '../pages/checkout'
// import ShowCasePage from '../pages/showCase'
// import AddPlayerPage from '../pages/addPlayer'
import { Switch } from 'react-router-dom'

export const AppRoutes = () => {
  return (
    <Switch>
      <UserRoute path="/login" component={LoginPage} />
      <UserRoute path="/register" component={RegisterPage} />
      {/* <ProtectedRoute path="/home" component={HomePage} />
      <ProtectedRoute path="/aboutUs" component={AboutUs} />
      <ProtectedRoute path="/checkout" component={CheckoutPage} />
      <ProtectedRoute path="/showCase" component={ShowCasePage} />
      <ProtectedRoute path="/addPlayer" component={AddPlayerPage} /> */}
      <ProtectedRoute path="*" component={HomePage} />
    </Switch>
  )
}
export default AppRoutes
