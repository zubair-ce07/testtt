/* Closures */

function Outer () {
  var me = 'Abdullah'
  return function Inner () {
    console.log(me + ' Zafar')
  }
}

const instance = Outer()

instance()

let val = 7
function createAdder () {
  function addNumbers (a, b) {
    let ret = a + b
    return ret
  }
  return addNumbers
}
let adder = createAdder()
let sum = adder(val, 8)
console.log('example of function returning a function: ', sum)

function createCounter () {
  let counter = 0
  const myFunction = function () {
    counter = counter + 1
    return counter
  }
  return myFunction
}
const increment = createCounter()
const c1 = increment()
const c2 = increment()
const c3 = increment()
console.log('example increment', c1, c2, c3)
