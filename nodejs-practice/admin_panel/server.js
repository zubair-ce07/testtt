var express = require('express');
var crypto = require('crypto');
var passport = require('passport');
var loginStatus = require('connect-ensure-login');
var Strategy = require('passport-local').Strategy;


// MONGO DB SETUP //

const MongoClient = require('mongodb').MongoClient;
const uri = "mongodb+srv://admin:admin@cluster0-ttgom.mongodb.net/test?retryWrites=true&w=majority";
const client = new MongoClient(uri, { useNewUrlParser: true });

var db;

console.log("Connecting to DB...");

client.connect(err => {
	console.log("Successfully Connected to DB...");
	db = client.db("users_test").collection("users_test");
});


// PASSWORD HASHING MECHANISM //

function genRandomString(length){
	return crypto.randomBytes(Math.ceil(length/2))
	.toString('hex')
	.slice(0,length);
}

function sha512(password, salt){
	var hash = crypto.createHmac('sha512', salt);
	hash.update(password);
	var value = hash.digest('hex');
	return {
		salt:salt,
		passwordHash:value
	}
}

function saltHashPassword(userpassword) {
	var salt = genRandomString(16);
	return sha512(userpassword, salt);
}


// UTILITY FUNCTIONS //

function viewUsers(req, res) {
	db.find((err, records)=> {
		records.toArray((err, array) => {
			res.json(array)
		})
	})
}


function addUser(req, res) {
	let userDetails = req.query

	if(!userDetails.username || !userDetails.name || !userDetails.admin || !userDetails.password) {
		res.json({response: "username, name, password, admin all MUST be provided!"})
		return
	}

	let passwordObject = saltHashPassword(userDetails.password)
	
	db.findOne({username: userDetails.username}, (err, result) => {
		if (err) {
			console.log(err);
			res.json({response: "Sorry, there was an error..."})
			return err;
		}
		
		if(result) {
			res.json({response: `Sorry, user with ${userDetails.username} already exists...`})
			return;
		} else {
			try {
				db.insertOne({
					username: userDetails.username, 
					name: userDetails.name, 
					admin: userDetails.admin, 
					password_hash: passwordObject.passwordHash, 
					password_salt: passwordObject.salt})
				res.json({response: `User ${userDetails.username} was successfully added!`});
			} catch (e) {
				res.json({response: "Sorry, there was an error..."})
				return err
			}
		}
	})
}


function deleteUser(req, res) {
	let usernameToDelete = req.query.username

	if(!usernameToDelete) {
		res.json({response: "Please specify a USERNAME to delete from database"});
		return;
	}
	
	try {
		db.deleteOne({username: usernameToDelete});
		res.json({response: `User ${usernameToDelete} was successfully deleted!`});
	} catch(e) {
		console.log(e)
		res.json({response: `Failed to delete the user: ${usernameToDelete}`})
	}
}


function updateUser(req, res) {
	let usernameToUpdate = req.query.username

	if(!usernameToUpdate) {
		res.json({response: "Please specify a USERNAME to `UPDATE` from database"});
		return;
	}
	
	try {
		db.findOne({username: usernameToUpdate}, (err, result) => {
			if(result) {
				let update = {}
				for(key in result) {
					if(key == "password") {
						continue;
					}
					if(key in req.query) {
						update[key] = req.query[key]
					} else {
						update[key] = result[key]
					}
				}
				if("password" in req.query) {
					let passwordObject = saltHashPassword(req.query["password"])
					update["password_hash"] = passwordObject.passwordHash
					update["password_salt"] = passwordObject.salt
				}
				db.updateOne({username: usernameToUpdate}, {$set: update})
				res.send({response: "Update applied"})
			} else {
				res.json({response: `No user with username ${usernameToUpdate} exists in the database`});
				return;
			}
		});
	} catch(e) {
		console.log(e)
		res.json({response: `Failed to update the user: ${usernameToUpdate}`})
	}
}

// PASSPORT JS SETUP //

passport.use(new Strategy(
function(username, password, cb) {
	db.findOne({username:username}, function(err, user) {
		if (!user) { return cb(null, false); }
		given_password_hash = sha512(password, user.password_salt).passwordHash
		if (err) {return cb(err); }
		if (given_password_hash != user.password_hash) { 
			console.log(given_password_hash);
			return cb(null, false, {message: "Wrong Password!"}); 
		}
		return cb(null, user);
	});
}));


passport.serializeUser(function(user, cb) {
	cb(null, user.username);
});


passport.deserializeUser(function(username, cb) {
	db.findOne({username: username}, function (err, user) {
		if (err) { return cb(err); }
		cb(null, user);
	});
});


// EXPRESS SETTINGS AND ROUTES //

var app = express();
app.use(express.urlencoded({ extended: true }));
app.use(require('express-session')({ secret: 'keyboard cat', resave: false, saveUninitialized: false }));
app.use(passport.initialize());
app.use(passport.session());


app.head('/', function (req, res) {
	res.end();
})


app.get('/', function(req, res) {
	if (req.user) {
		res.json({response: "Hi there! You are now logged in..."})
	} else {
		res.json({response: "Please log in.."});
	}
});


app.post('/',
	passport.authenticate('local', { failureRedirect: '/'}),
	function(req, res) {
		res.redirect('/');
});


app.get('/viewUsers', function (req, res) {
	viewUsers(req, res)
});


app.put('/',
	loginStatus.ensureLoggedIn('/'),
	function (req, res) {
		addUser(req, res)
})


app.get('/logout',
	function(req, res){
		req.logout();
		res.redirect('/');
});


app.options('/',
	function(req, res) {
		res.send("GET, POST, HEAD, PUT, DELETE, OPTIONS")
})


app.patch('/',
	function(req, res) {
		updateUser(req, res);
})


app.delete('/', 
	loginStatus.ensureLoggedIn('/'),
	function (req, res) {
		deleteUser(req, res);
})


app.get('/profile',
	loginStatus.ensureLoggedIn('/'),
	function(req, res) {
		let user = req.user;
		res.json({userDetails: {
			id: user.id,
			username: user.username,
			name: user.name,
			admin: user.admin
		}
	});
});

app.listen(8080);
