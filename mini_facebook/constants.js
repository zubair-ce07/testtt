const  BASEURL = 'http://localhost:3000';

const MONTHS = [
  `January`, `February`, `March`, `April`, `May`,
  `June`, `July`, `August`, `September`,
  `October`, `November`, `December`
];

const LOGIN_ERROR = `Invalid username or password`
const USERNAME_ERROR = `Already registered, try another.`
const SUCESSFULLY_REGISTERED_MSG = `Successfully registered.`

const PASSWORD_ERROR = {
  "length": `Passwords length must be between 5 and 20`,
  "regex":  `Password must have at least 1 uppercase,1 digit and a special character.`,
  "misMatched": `Password mismatched`
}

const MOBILE_ERROR = {
  "notDigit": `Characters are not allowed`,
  "length":  `Mobile Number must be 10 digits only`
}

const NEW_POST_SUCCESS_MSG = `your post has been posted...`
