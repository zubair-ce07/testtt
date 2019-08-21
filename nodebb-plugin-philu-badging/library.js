"use strict";

var controllers = require("./src/controllers");
var routes = require("./src/routes");

var library = {};

library.init = function (params, callback) {

    routes.init(params, controllers, callback);

    callback();
};

module.exports = library;
