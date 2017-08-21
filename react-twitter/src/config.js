let domain = "http://127.0.0.1:8000/api";
export {domain};
function getUserToken() {
    return localStorage.user ? JSON.parse(localStorage.user).token : null;
}
export function getHeader() {
    return {
        Authorization: 'Token ' + getUserToken(),
        'Content-Type': 'application/json',
    };
}
