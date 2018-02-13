// Enemies our player must avoid
var Enemy = function(x,y, speed) {
    // Variables applied to each of our instances go here,
    // we've provided one for you to get started
    this.x = x;
    this.y = y;
    this.speed = speed;
    // The image/sprite for our enemies, this uses
    // a helper we've provided to easily load images
    this.sprite = 'images/enemy-bug.png';
};

// Update the enemy's position, required method for game
// Parameter: dt, a time delta between ticks
Enemy.prototype.update = function(dt) {
    // You should multiply any movement by the dt parameter
    // which will ensure the game runs at the same speed for
    // all computers.
    x_range = [this.x - 80, this.x + 80];
    y_range = [this.y - 50, this.y + 50];
    if ((player.x >= x_range[0] && player.x <= x_range[1]) && (player.y >= y_range[0] && player.y <= y_range[1]))
    {
        resetBoard();
        console.log('YOU LOSE')
    }
    this.x += this.speed*dt;
    if (this.x >= 500)
    {
        this.x = 0;
    }

};

// Draw the enemy on the screen, required method for game
Enemy.prototype.render = function() {
    ctx.drawImage(Resources.get(this.sprite), this.x, this.y);
};

Enemy.prototype.reset = function(x,y){
    this.x = x;
    this.y = y;
}

// Now write your own player class
// This class requires an update(), render() and
// a handleInput() method.
var Player = function(x,y){
    this.x = x;
    this.y = y;
    this.sprite = 'images/char-boy.png';
};

Player.prototype.render = function(){
       ctx.drawImage(Resources.get(this.sprite), this.x, this.y);
};

Player.prototype.update = function(x, y){
    x < 0 ? x=0 : (x > 420? x = 420 : (y < 0? y = -30 : (y > 420? y = 420 : y = y)))
     this.x = x;
    this.y = y;
    if (this.y == -30)
    {

        this.y = 330;
        console.log('YOU win');
    }

};

Player.prototype.reset = function(){
    this.x = 280;
    this.y = 320;
};

Player.prototype.handleInput = function(action){
    switch(action){
        case  'left':{
            this.update(this.x-50, this.y);
            break;
        }
        case 'right':{
            this.update(this.x+50, this.y);
            break;
        }
        case 'up':{
            this.update(this.x, this.y-50);
            break;
        }
        case 'down':{
            this.update(this.x, this.y+50);
            break;
        }

    }
};

player = (new Player(280,320));


// Now instantiate your objects.
// Place all enemy objects in an array called allEnemies
// Place the player object in a variable called player
var speed = 50;
var allEnemies = [];
allEnemies.push(new Enemy(Math.ceil(Math.random()*500),60,speed));
allEnemies.push(new Enemy(Math.ceil(Math.random()*500),140,speed));
allEnemies.push(new Enemy(Math.ceil(Math.random()*500),230,speed));

function resetBoard(){
    player.reset();
    allEnemies[0].reset(Math.ceil(Math.random()*500),60);
    allEnemies[1].reset(Math.ceil(Math.random()*500),140);
    allEnemies[2].reset(Math.ceil(Math.random()*500),230);

};

// This listens for key presses and sends the keys to your
// Player.handleInput() method. You don't need to modify this.
document.addEventListener('keyup', function(e) {
    var allowedKeys = {
        37: 'left',
        38: 'up',
        39: 'right',
        40: 'down'
    };
    player.handleInput(allowedKeys[e.keyCode]);
});
