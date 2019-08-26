"use strict";

const {
    initializeConfigCollection,
    getAllConfig,
    updateConfigById,
    deleteConfigById
} = require('./src/controllers')

const {
    BADGING_BASE_URL
} = require('./constants');

var library = {}; 

library.init = function (params, callback) {
    initializeConfigCollection();
    callback();
};

library.handleNewRoutes = function (params, callback) {
    const router = params.router;
    const { requireUser, requireAdmin } = params.apiMiddleware;
    router.use(requireUser, requireAdmin);

    router.get(BADGING_BASE_URL, getAllConfig);
    router.post(`${BADGING_BASE_URL}/:badgeId`, updateConfigById);
    router.delete(`${BADGING_BASE_URL}/:badgeId`, deleteConfigById);

    callback(null, params);
}

module.exports = library;
 