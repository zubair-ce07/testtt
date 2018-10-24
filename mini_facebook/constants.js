const  BASEURL = 'http://localhost:3000';

const MONTHS = [
  `January`, `February`, `March`, `April`, `May`,
  `June`, `July`, `August`, `September`,
  `October`, `November`, `December`
];

LOGIN_ERROR = `Invalid username or password`
USERNAME_ERROR = `Already registered, try another.`
SUCESSFULLY_REGISTERED_MSG = `Successfully registered.`

PASSWORD_ERROR = {
  "length": `Passwords length must be between 5 and 20`,
  "regex":  `Password must have at least 1 uppercase,1 digit and a special character.`,
  "misMatched": `Password mismatched`
}

MOBILE_ERROR = {
  "notDigit": `Characters are not allowed`,
  "length":  `Mobile Number must be 10 digits only`
}

NEW_POST_SUCCESS_MSG = `your post has been posted...`
