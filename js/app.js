let tileWidth = 101;
let tileHeight = 85;

var randomPosition = function (max, min) {
    // from: https://stackoverflow.com/questions/4550505/getting-a-random-value-from-a-javascript-array
    return (Math.floor(Math.random() * (+max - +min)) + +min);
}

// Enemies our player must avoid
var Enemy = function() {
    // Variables applied to each of our instances go here,
    // we've provided one for you to get started

    // The image/sprite for our enemies, this uses
    // a helper we've provided to easily load images
    this.numTicks = 0;
    this.sprite = 'images/enemy-bug.png';
    this.x = -tileWidth*randomPosition(3,1)
    this.y = tileHeight*randomPosition(6,1) - 30
};

// Update the enemy's position, required method for game
// Parameter: dt, a time delta between ticks
Enemy.prototype.update = function(dt) {
    if(this.x + tileWidth*dt > 101*5){
        this.x = -tileWidth*randomPosition(3,1)
        this.y = tileHeight*randomPosition(6,1) - 30
    } else {
        this.x += tileWidth*dt
    }
    // You should multiply any movement by the dt parameter
    // which will ensure the game runs at the same speed for
    // all computers.
};

// Draw the enemy on the screen, required method for game
Enemy.prototype.render = function() {
    ctx.drawImage(Resources.get(this.sprite), this.x, this.y);
};

// Now write your own player class
// This class requires an update(), render() and
// a handleInput() method.

var Player = function() {
    this.sprite = 'images/char-boy.png';
    this.x = tileWidth*2;
    this.y = tileHeight*5 - 30;
};

Player.prototype.update = function(key_pressed) {
    if(key_pressed == 'up') {
        this.y -= tileHeight
        if(this.y <= 0){
            this.y = tileHeight*5 - 30
        }
    } else if (key_pressed == 'down') {
        this.y += tileHeight
        if(this.y >= tileHeight*5 - 30){
            this.y = tileHeight*5 - 30
        }
    } else if (key_pressed == 'left') {
        this.x -= tileWidth
        if(this.x <= -tileWidth){
            this.x = 0
        }
    } else if (key_pressed == 'right') {
        this.x += tileWidth
        if(this.x >= tileWidth*4){
            this.x = tileWidth*4
        }
    }
};

Player.prototype.render = function() {
    ctx.drawImage(Resources.get(this.sprite), this.x, this.y);
};

Player.prototype.handleInput = function(key_pressed) {
    this.update(key_pressed)
};

// Now instantiate your objects.
// Place all enemy objects in an array called allEnemies
// Place the player object in a variable called player
var allEnemies = [new Enemy(), new Enemy(), new Enemy()]
var player = new Player();


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
