import React from "react";
import { BrowserRouter as Switch, Route } from "react-router-dom";
import Landing from "./components/landing";
import IconItems from "./components/iconItems";

const Routes = () => {
  return (
    <Switch>
      <Route exact path={routes.index.path} component={Landing} />
      <Route exact path={routes.iconsList.path} component={IconItems} />
    </Switch>
  );
};

export const routes = {
  index: {
    path: "/magic-app/"
  },
  iconsList: {
    path: "/magic-app/icons-list/"
  }
};

export default Routes;
