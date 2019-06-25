/* PROMISES - Chaining */
// PRINTS OUT HELLO 5 TIMES AFTER 1 SECOND EACH

function delayer (duration, num) {
  return new Promise(function (resolve, reject) {
    setTimeout(() => resolve(++num), duration)
  })
}

delayer(1000, 0).then((num) => {
  console.log('Hello, ' + num + '!')
  delayer(1000, num).then((num) => {
    console.log('Hello, ' + num + '!')
    delayer(1000, num).then((num) => {
      console.log('Hello, ' + num + '!')
      delayer(1000, num).then((num) => {
        console.log('Hello, ' + num + '!')
        delayer(1000, num).then((num) => {
          console.log('Hello, ' + num + '!')
        })
      })
    })
  })
})

// APPROACH 2 - AVOIDING CALLBACK HELL

delayer(1000, 0)
  .then((num) => {
    console.log('Hello, ' + num + '!')
    return delayer(1000, num)
  })
  .then((num) => {
    console.log('Hello, ' + num + '!')
    return delayer(1000, num)
  })
  .then((num) => {
    console.log('Hello, ' + num + '!')
    return delayer(1000, num)
  })
  .then((num) => {
    console.log('Hello, ' + num + '!')
    return delayer(1000, num)
  })
  .then((num) => {
    console.log('Hello, ' + num + '!')
    return delayer(1000, num)
  })

// USING Promise.all()
// completes after 3.5 seconds as per the second Promise
Promise.all([
  delayer(1000, 0),
  delayer(3500, 2.5),
  delayer(500, -0.5)
]).then((arr) => console.log(arr))

// USING Promise.race()
// completes after 500ms as per the third Promise
Promise.race([
  delayer(1000, 0),
  delayer(3500, 2.5),
  delayer(500, -0.5)
]).then((arr) => console.log(arr))
