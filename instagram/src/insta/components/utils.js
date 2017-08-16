// // export
//
// // const validateUsernameEmail = (data, value, name) => {
// //     const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
// //     if(data.is_taken === true || value.length < 1) {
// //         if(name === 'email'){
// //             document.styleSheets[1]['rules'][11].style.borderColor =
// //             "rgb(255, 51, 51)"
// //         } else {
// //             document.styleSheets[1]['rules'][12].style.borderColor =
// //                 "rgb(255, 51, 51)"
// //         }
// //     } else if(name === 'email') {
// //         if(re.test(value) === false){
// //             document.styleSheets[1]['rules'][11].style.borderColor =
// //             "rgb(255, 51, 51)"
// //         } else {
// //             document.styleSheets[1]['rules'][11].style.borderColor =
// //                 "rgb(0, 204, 102)"
// //         }
// //     } else {
// //         document.styleSheets[1]['rules'][12].style.borderColor =
// //             "rgb(0, 204, 102)";
// //     }
// // };
//
// const validateFirstName = (data, value, name) => {
//     if(value.length <2) {
//         document.styleSheets[1]['rules'][13].style.borderColor =
//                     "rgb(255, 51, 51)"
//     } else {
//         document.styleSheets[1]['rules'][13].style.borderColor =
//                 "rgb(0, 204, 102)";
//     }
// };
//
// // export default *
// // validateUsernameEmail;
// // export default validateFirstName;
//
// // module.exports = {
// //     one: validateUsernameEmail,
// //     two: validateFirstName,
// // };