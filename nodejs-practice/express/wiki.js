var express = require('express')

var router = express.Router();

router.get('/', (req, res) => {
    res.sendFile('wiki/wiki.html', {root: __dirname });
})

router.get('/info', (req, res) => {
    res.send('This is your info');
})

module.exports = router;
