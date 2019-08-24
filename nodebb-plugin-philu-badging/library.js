"use strict";

var controllers = require("./src/controllers");
var utils = require("./src/utils");

const {
    BADGING_BASE_URL
} = require('./constants');

var library = {}; 

library.init = function (params, callback) {
    utils.initializeConfigCollection();
    callback();
};

library.handleNewRoutes = function (params, callback) {
    const router = params.router;
    const { requireUser, requireAdmin } = params.apiMiddleware;
    router.use(requireUser, requireAdmin);

    router.get(BADGING_BASE_URL, controllers.getAllConfig);
    router.post(`${BADGING_BASE_URL}/:badgeId`, controllers.updateConfigById);
    router.delete(`${BADGING_BASE_URL}/:badgeId`, controllers.deleteConfigById);

    callback(null, params);
}

module.exports = library;
