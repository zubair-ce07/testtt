'use strict';

var assert = require('chai').assert;
require('./pre-require-fix');

var utils = require("../src/utils");

const {
  BADGE_CONFIG_KEY
} = require("../constants")

describe('Initialization', function() {

  describe('configuration initialization', function() {
    // db.count = function (configuration) {return 1}

    it('should resolve the promise when value already exists', function() {
        assert.equal(utils.initializeConfigCollection(), "key inserted!")
    })
  });
});
