export const required = value => (value ? undefined : "Required");
export const mustBeNumber = value => (isNaN(value) ? "Must be a number" : undefined);
export const minValue = min => value =>
    isNaN(value) || value >= min ? undefined : `Should be greater than ${min - 1}`;

export const minLength = min => value => value.length >= min ? undefined : `Should be greater than ${min - 1}`
export const isValidEmail = email => /^[^@]+@[^@]+\.[^@]{3}$/.test(email)
export const isPasswordMatch = (pass1, pass2) => pass1 === pass2