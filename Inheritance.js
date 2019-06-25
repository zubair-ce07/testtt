/* Inheritance */

function Person (first, last, age, gender, interests) {
  this.name = {
    first,
    last
  }
  this.age = age
  this.gender = gender
  this.interests = interests
};

Person.prototype.greeting = function () {
  return ('Hi! I\'m ' + this.name.first + '.')
}

var p1 = new Person('Atif', 'Aslam', 35, 'M', 'Music')
console.log(p1.greeting())

function Teacher (first, last, age, gender, interests, subject) {
  Person.call(this, first, last, age, gender, interests)
  this.subject = subject
}

Teacher.prototype = Object.create(Person.prototype)
Teacher.prototype.constructor = Teacher

Teacher.prototype.greeting = function () {
  return ('Hi Students! I\'m ' + this.name.first + '.')
}

var p2 = new Teacher('Karim', 'Nawaz', 45, 'M', 'Music', 'Computer Science')
console.log(p2.greeting())
