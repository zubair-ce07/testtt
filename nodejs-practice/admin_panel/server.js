var express = require('express');
var crypto = require('crypto');
var passport = require('passport');
var flash = require('connect-flash')
var Strategy = require('passport-local').Strategy;
const MongoClient = require('mongodb').MongoClient;
const uri = "mongodb+srv://admin:admin@cluster0-ttgom.mongodb.net/test?retryWrites=true&w=majority";
const client = new MongoClient(uri, { useNewUrlParser: true });

var genRandomString = function(length){
  return crypto.randomBytes(Math.ceil(length/2))
          .toString('hex')
          .slice(0,length);
};

var sha512 = function(password, salt){
  var hash = crypto.createHmac('sha512', salt);
  hash.update(password);
  var value = hash.digest('hex');
  return {
      salt:salt,
      passwordHash:value
  };
};

function saltHashPassword(userpassword) {
  var salt = genRandomString(16);
  return sha512(userpassword, salt);
}


function viewUsers(req, res) {
  db.find((err, records)=> {
    res.render('viewUsers', {records: records})
  })
}

function addUser(req, res) {
  let userDetails = req.body
  let passwordObject = saltHashPassword(req.body.password)

  if(userDetails.admin) {
    db.count().then((count)=> {
      db.insertOne({ id: count+1,
        username: userDetails.username, 
        name: userDetails.name, 
        admin: true, 
        password_hash: passwordObject.passwordHash, 
        password_salt: passwordObject.salt})
    })
    res.render('addUser', {success: 1, failed: 0});
  } else {
    db.count().then((count)=> {
      db.insertOne({ id: count+1,
        username: userDetails.username, 
        name: userDetails.name, 
        admin: false, 
        password_hash: passwordObject.passwordHash, 
        password_salt: passwordObject.salt})
    })
    res.render('addUser', {success: 1, failed: 0});
  }
}

console.log("Connecting to DB...");
var db;

client.connect(err => {
    console.log("Successfully Connected to DB...");
    db = client.db("users_test").collection("users_test");
});


passport.use(new Strategy(
  function(username, password, cb) {
    db.findOne({username:username}, function(err, user) {
      if (!user) { return cb(null, false); }
      given_password_hash = sha512(password, user.password_salt).passwordHash
      if (err) { return cb(err); }
      if (given_password_hash != user.password_hash) { 
        console.log(given_password_hash); 
        console.log(user.password_hash); 
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


var app = express();


app.set('views', __dirname + '/views');
app.set('view engine', 'ejs');

app.use(flash())
app.use(express.urlencoded({ extended: true }));
app.use(require('express-session')({ secret: 'keyboard cat', resave: false, saveUninitialized: false }));

app.use(passport.initialize());
app.use(passport.session());


app.get('/',
  function(req, res) {
    res.render('home', { user: req.user });
  });

app.get('/login',
  function(req, res){
    // console.log(req.flash("error"))
    res.render('login', { user: req.user, error: req.flash('error')});
  });
  
app.post('/login', 
  passport.authenticate('local', { failureRedirect: '/login', failureFlash: true}),
  function(req, res) {
    res.redirect('/');
  });

app.get('/addUser',
function(req, res) {
  res.render('addUser', {success: 0, failed: 0});
});

app.get('/viewUsers', function (req, res) {
  viewUsers(req, res)
});

app.post('/addUser', function (req, res) {
  addUser(req, res)
})
  
app.get('/logout',
  function(req, res){
    req.logout();
    res.redirect('/');
  });

app.get('/profile',
  require('connect-ensure-login').ensureLoggedIn(),
  function(req, res){
    res.render('profile', { user: req.user });
  });

app.listen(8080);
