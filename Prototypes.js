/* Prototypes */

function Human (first, last) {
  this.firstname = first
  this.lastname = last
  this.print = function () {
    return this.firstname + ' ' + this.lastname
  }
}

var p1 = new Human('Atif', 'Aslam')
var p2 = new Human('Arif', 'Lohar')

Human.prototype.Country = 'Pakistan'

console.log(p1.print() + ' ' + p1.Country)
console.log(p2.print() + ' ' + p2.Country)

p1.Country = 'The United Kingdom'
console.log(p1.print() + ' ' + p1.Country)
console.log(p2.print() + ' ' + p2.Country)

console.log(Object.getPrototypeOf(p1))
console.log(Human.prototype)
console.log(Object.getPrototypeOf(p1) === Human.prototype)
