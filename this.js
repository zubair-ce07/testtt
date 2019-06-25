/* `this` keyword */

function Test1 () {
  return this
}

let Test2 = function () {
  return this
}

console.log(Test1()) // refers to global execution context
console.log(new Test1()) // refers to lexical/functional scope of the newly created object

// Same goes for function expressions
console.log(Test2()) // refers to global execution context
console.log(new Test2()) // refers to lexical/functional scope of the newly created object

/* IIFEs does have access to outside context */
console.log(
  (function () {
    return this
  })()
);

// with `new` instance, local context is returned
(function () {
  function Fg () { this.th = 'th'; return this }
  console.log(new Fg())
})();

// without creating a `new` instance, all variables declared inside are also part of the global
(function () {
  function Fg () { this.th = 'th'; return this }
  console.log(Fg())
})()
