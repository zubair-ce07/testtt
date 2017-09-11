let domain = "http://127.0.0.1:8000/api";
export {domain};
function getUserToken() {
    return localStorage.user ? JSON.parse(localStorage.user).token : null;
}
export function getHeader() {
    if (getUserToken()) {
        return {
        Authorization: 'Token ' + getUserToken(),
        'Content-Type': 'application/json',
        };
    }
    return {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }
}
