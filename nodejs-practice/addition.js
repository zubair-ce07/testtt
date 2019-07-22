var add = require('./additionModule.js')

let first = process.argv[2]
let second = process.argv[3]

console.log(add.add(+first, +second))
