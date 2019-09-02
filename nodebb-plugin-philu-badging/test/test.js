'use strict';

const httpMocks = require('node-mocks-http')
var assert = require('chai').assert;
require('./pre-require-fix');


const {
  initializeConfigCollection,
  getAllConfig,
  updateConfigById,
  deleteConfigById
} = require('../src/controllers');

const {
  BADGE_CONFIG_KEY
} = require("../constants");


describe('Testing initialization of configuration collection:', function() {
  describe('Empty configuration collection at the start:', function() {
    it('Should return status code 204 at the beginning', function() {
        const req = httpMocks.createRequest()
        const res = httpMocks.createResponse()
        getAllConfig(req, res)
        .then(() => {
          assert.equal(res._getStatusCode(), 204)
        })
        .catch((e) => {
          console.log(e)
        });
    })
  });

  describe('Initializing collection for badging:', function() {
    it('should return "Configuration successful" message', function() {
        initializeConfigCollection()
        .then((configResponse) => {
          assert.equal(configResponse, "Configuration successful")
        })
        .catch((e) => {
          console.log(e)
        });
    })
  });

  describe('Checking initialized collection:', function() {
    it('res should have `{}` in response data', function() {
        const req = httpMocks.createRequest()
        const res = httpMocks.createResponse()
        getAllConfig(req, res)
        .then(() => {
          assert.equal(res._getData(), `{}`)
        })
        .catch((e) => {
          console.log(e)
        });
    })
  });

});


describe('Testing configuration insertion', function() {
  describe('Adding a new key without required parameters:', function() {
    describe('Adding a new key without badge type:', function() {
      it('Should return status code 400 with error message', function() {
          const req = httpMocks.createRequest()
          const res = httpMocks.createResponse()

          req.params.badgeId = 23;
          req.body.threshold = 500;
  
          updateConfigById(req, res)
          .then(() => {
            assert.equal(res._getStatusCode(), 400)
          })
          .catch((e) => {
            console.log(e)
          });
      })
    });

    describe('Adding a new key without badgeId:', function() {
      it('Should return status code 400 with error message', function() {
          const req = httpMocks.createRequest()
          const res = httpMocks.createResponse()

          req.body.type = "team";
          req.body.threshold = 500;
  
          updateConfigById(req, res)
          .then(() => {
            assert.equal(res._getStatusCode(), 400)
          })
          .catch((e) => {
            console.log(e)
          });
      })
    });

    describe('Adding a new key without badge threshold:', function() {
      it('Should return status code 400 with error message', function() {
          const req = httpMocks.createRequest()
          const res = httpMocks.createResponse()

          req.params.badgeId = 23;
          req.body.type = "team";
  
          updateConfigById(req, res)
          .then(() => {
            assert.equal(res._getStatusCode(), 400)
          })
          .catch((e) => {
            console.log(e)
          });
      })
    });
  });

  describe('Adding a new key with wrong badge type:', function() {
    it('Should return status code 400 with error message', function() {
        const req = httpMocks.createRequest()
        const res = httpMocks.createResponse()

        req.params.badgeId = 23;
        req.body.type = "random";
        req.body.threshold = 500;

        updateConfigById(req, res)
        .then(() => {
          assert.equal(res._getStatusCode(), 400)
        })
        .catch((e) => {
          console.log(e)
        });
    })
  });

  describe('Adding a new key with wrong threshold:', function() {
    it('Should return status code 400 with error message', function() {
        const req = httpMocks.createRequest()
        const res = httpMocks.createResponse()

        req.params.badgeId = 23;
        req.body.type = "random";
        req.body.threshold = 0;
        
        updateConfigById(req, res)
        .then(() => {
          assert.equal(res._getStatusCode(), 400)
        })
        .catch((e) => {
          console.log(e)
        });
    })
  });

  describe('Adding a new key with CORRECT PARAMS:', function() {
    const req = httpMocks.createRequest()
    const res = httpMocks.createResponse()

    req.params.badgeId = 123;
    req.body.type = "conversationalist";
    req.body.threshold = 150;

    it('Should return status code 200 with success message', function() {
        
        
        updateConfigById(req, res)
        .then(() => {
          assert.equal(res._getStatusCode(), 200)
          assert.equal(res._getJSONData().message, 'Key updated successfully!')
        })
        .catch((e) => {
          console.log(e)
        });
    })

    describe('Testing added key:', function() {
      it('Should return config added in last test', function() {
          const req = httpMocks.createRequest()
          const res = httpMocks.createResponse()
          getAllConfig(req, res)
          .then(() => {
            assert.equal(res._getJSONData()['123'].type, 'conversationalist')
            assert.equal(res._getJSONData()['123'].threshold, 150)
          })
          .catch((e) => {
            console.log(e)
          });
      })
    });
  
  });
})


describe('Updating an existing key:', function() {
  const req = httpMocks.createRequest()
  const res = httpMocks.createResponse()

  req.params.badgeId = 123;
  req.body.type = "conversationalist";
  req.body.threshold = 300;

  it('Should return status code 200 with success message', function() {
      
      
      updateConfigById(req, res)
      .then(() => {
        assert.equal(res._getStatusCode(), 200)
        assert.equal(res._getJSONData().message, 'Key updated successfully!')
      })
      .catch((e) => {
        console.log(e)
      });
  })

  describe('Testing added key:', function() {
    it('Should return config updated in last test', function() {
        const req = httpMocks.createRequest()
        const res = httpMocks.createResponse()
        getAllConfig(req, res)
        .then(() => {
          assert.equal(res._getJSONData()['123'].type, 'conversationalist')
          assert.equal(res._getJSONData()['123'].threshold, 300)
        })
        .catch((e) => {
          console.log(e)
        });
    })
  });
});


describe('Deleting an existing key:', function() {
  const req = httpMocks.createRequest()
  const res = httpMocks.createResponse()

  req.params.badgeId = 123;

  it('Should return status code 200 with deletion success message', function() {
      deleteConfigById(req, res)
      .then(() => {
        assert.equal(res._getStatusCode(), 200)
        assert.equal(res._getJSONData().message, 'Key deleted successfully!')
      })
      .catch((e) => {
        console.log(e)
      });
  })


  it('Should return status code 204', function() {
    deleteConfigById(req, res)
    .then(() => {
      assert.equal(res._getStatusCode(), 204)
    })
    .catch((e) => {
      console.log(e)
    });
  })
});
