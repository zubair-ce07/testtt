const joi = require("@hapi/joi")

exports.addUserValidation = joi.object().keys({
    username: joi.string().alphanum().min(3).max(25).required(),
    name: joi.string().min(2).max(50).required(),
    admin: joi.string().default("false"),
    password: joi.string().required().min(3).max(25)
});
