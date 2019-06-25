/* HOISTING - 1 */
console.log(a);
var a = 'A' // Outputs `undefined` because of `var` hoisting

// console.log(b) // Gives `ReferenceError`, since `let` is not hoisted 
let b = 'B' 

// console.log(c) // Also gives `ReferenceError`, since `const` is not hoisted
const c = 'C'


/* HOISTING - 2 */
scope(); // function declarations are completely hoisted, called before declaration
function scope() {
    console.log('declarations')
}

// only variable declaration is hoisted. Declarations take priority over expressions!!
var scope = function() {
    console.log('expression')
}

scope(); // function declarations are completely hoisted

/* BLOCK LEVEL SCOPE */
for (var d = 0; d < 5; d++) {
    console.log(d);
}

console.log(d) // `var` does not support block level scope, `let` does


/* SHADOWING - 1 */
var test = 'GLOBAL';

function testScope(){
    var test = 'LOCAL'
    console.log(test)
};

testScope(); // `test` shadowed. Search starts from innermost scope
console.log(test); // `test` in global scope is accessed


/* SHADOWING - 2 (variable not declared) */
var test = 'GLOBAL';

function testScope(){
    test = 'LOCAL' // varialbe not declared, overwrites the global one
    console.log(test)
};

console.log(test); // `test` in global scope is accessed
testScope(); // `test` shadowed. But overwrites the global one on execution
console.log(test); // overwritten `test` in global scope is accessed


