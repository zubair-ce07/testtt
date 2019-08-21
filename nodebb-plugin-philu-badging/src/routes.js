'use strict';

var routes = module.exports;

routes.init = function (params, controllers, callback) {
    params.router.post('/api/saveConfig', [], controllers.saveConfiguration);
};
