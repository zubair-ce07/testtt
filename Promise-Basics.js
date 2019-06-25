/* PROMISES - Basic 1 */

function summer (num) {
  return new Promise(function (resolve, reject) {
    if (num >= 999999999) {
      reject(new Error('Too big a number'))
    } else {
      let sum = 0
      for (let i = 0; i < num; i++) {
        sum += i
      }
      resolve(sum)
    }
  })
}

// 1. summer(999999999) call scheduled and the execution moves on to line 26
// 4. Promise rejected and returned, result available and printed
summer(999999999).catch(
  function (err) {
    console.log(err)
  }
)

// 2. first thing that gets printed
console.log('In the middle')

// 3. summer(931344420) call scheduled and the execution moves on to line 19
// 5. Promise resolved and returned, result available and printed
summer(931344420).then(
  function (sum) {
    console.log(sum)
  }
)

/* PROMISES - Basic 2 */

function delayer (duration) {
  return new Promise(function (resolve, reject) {
    if (duration >= 2000) {
      reject(new Error('Too long!'))
    } else {
      setTimeout(() => resolve('Done ' + duration), duration)
    }
  })
}

// 1. delayer(2000) call scheduled and the execution moves on to line 55
// 4. Promise rejected and returned, result available and printed
delayer(2000).catch(
  (err) => console.log(err.name)
)

// 2. first thing that gets printed
console.log('Middle')

// 3. delayer(1500) call scheduled and the execution moves on to line 50
// 5. Promise resolved and returned, result available and printed
delayer(1500).then(
  (res) => console.log(res)
)
