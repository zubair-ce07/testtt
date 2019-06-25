/* Different ways to create an object in JS */

// 1. Using Object Literals
var objectLiteralWay = {
  first: '',
  last: '',
  print: function () {
    return this.firstname + ' ' + this.lastname
  }
}
console.log(objectLiteralWay)

// 2. Using the Global object as base
// eslint-disable-next-line no-new-object
var newObjectWay = new Object()
newObjectWay['first'] = ''
newObjectWay['last'] = ''
newObjectWay.print = function () {
  return this.firstname + ' ' + this.lastname
}

// 3. Using Constructor functions
function Human (first, last) {
  this.firstname = first
  this.lastname = last
  this.print = function () {
    return this.firstname + ' ' + this.lastname
  }
}

var p1 = new Human('Atif', 'Aslam')
var p2 = new Human('Arif', 'Lohar')

console.log(p1.print())
console.log(p2.print())
