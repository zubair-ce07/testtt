/* ASYNC-AWAIT */
// PRINTS OUT HELLO 5 TIMES AFTER 1 SECOND EACH

function delayer (duration, num) {
  return new Promise(function (resolve, reject) {
    setTimeout(() => resolve(++num), duration)
  })
}

(async () => {
  let num = await delayer(1000, 0)
  console.log('Hello, ' + num + '!')
  num = await delayer(1000, num)
  console.log('Hello, ' + num + '!')
  num = await delayer(1000, num)
  console.log('Hello, ' + num + '!')
  num = await delayer(1000, num)
  console.log('Hello, ' + num + '!')
  num = await delayer(1000, num)
  console.log('Hello, ' + num + '!')
})()
