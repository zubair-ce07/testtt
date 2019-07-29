var crypto = require('crypto');

exports.genRandomString =  function (length){
	return crypto.randomBytes(Math.ceil(length/2))
	.toString('hex')
	.slice(0,length);
}

exports.sha512 = function (password, salt){
	var hash = crypto.createHmac('sha512', salt);
	hash.update(password);
	var value = hash.digest('hex');
	return {
		salt:salt,
		passwordHash:value
	}
}
