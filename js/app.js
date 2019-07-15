// Globals
let tileWidth = 101;
let tileHeight = 85;
var finished = 0;
var lives = 5;
var tryAgain = false;
var pause = false;
var started = false;

// Helper function
// https://stackoverflow.com/questions/4550505/getting-a-random-value-from-a-javascript-array
var randomPosition = function (max, min) {
    return (Math.floor(Math.random() * (+max - +min)) + +min);
}

// Helper function
// https://stackoverflow.com/questions/6454198/check-if-a-value-is-within-a-range-of-numbers
function between(x, min, max) {
    return x >= min && x <= max;
}

// Enemies our player must avoid
var Enemy = function() {
    this.sprite = 'images/enemy-bug.png';
    this.x = -tileWidth*randomPosition(10,1)
    this.y = tileHeight*randomPosition(5,1) - 30
};

// Update the enemy's position, required method for game
// Parameter: dt, a time delta between ticks
Enemy.prototype.update = function(dt) {
    if(this.x + tileWidth*dt > 101*5){
        this.x = -tileWidth*randomPosition(6,1)
        this.y = tileHeight*randomPosition(5,1) - 30
    } else {
        this.x += tileWidth*dt
    }
};

// Draw the enemy on the screen, required method for game
Enemy.prototype.render = function() {
    ctx.drawImage(Resources.get(this.sprite), this.x, this.y);
};


var Player = function() {
    this.sprite = 'images/char-boy.png';
    this.x = tileWidth*2;
    this.y = tileHeight*5 - 30;
};

Player.prototype.update = function(key_pressed) {
    if(key_pressed == 'up') {
        this.y -= tileHeight
        for(let i = 0; i<playerList.length; i++){
            current = playerList[i]
            if(this.x == current.x && this.y == current.y){
                this.y += tileHeight;
                break;
            }
        }
        if(this.y <= 0){
            finished += 1
            playerList.push(player)
            player = new Player()
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
    
    for (let i = 0; i < allEnemies.length; i++){
        if(between(this.x, allEnemies[i].x - 70, allEnemies[i].x + 70) &&
           between(this.y, allEnemies[i].y - 51, allEnemies[i].y + 51)) {
            this.x = tileWidth*2;
            this.y = tileHeight*5 - 30
            lives -= 1;
            break;
        }
    }

    document.getElementById("finished").innerHTML = `Finished: ${finished}`;
    document.getElementById("lives").innerHTML = `Lives: ${lives}`;
};

Player.prototype.render = function() {
    ctx.drawImage(Resources.get(this.sprite), this.x, this.y);
    for(let i = 0; i<playerList.length; i++){
        current = playerList[i]
        ctx.drawImage(Resources.get(current.sprite), current.x, current.y);
    }
};

Player.prototype.handleInput = function(key_pressed) {
    this.update(key_pressed)
};

// Now instantiate your objects.
// Place all enemy objects in an array called allEnemies
// Place the player object in a variable called player
var allEnemies = new Array(new Enemy(), new Enemy(), new Enemy(), 
                           new Enemy(), new Enemy(), new Enemy(), 
                           new Enemy())
var player = new Player();
var playerList = []


// This listens for key presses and sends the keys to your
// Player.handleInput() method. You don't need to modify this.
document.addEventListener('keyup', function(e) {
    var allowedKeys = {
        37: 'left',
        38: 'up',
        39: 'right',
        40: 'down'
    };

    if(started && !pause){
        player.handleInput(allowedKeys[e.keyCode]);
    }
    
});

window.onload = () => {
    var startID = setTimeout(() => {
                
    }, 2147483647);

    document.getElementById("pause").addEventListener("click", () => {
        if (started){
            pause = !pause
        }

        if(pause) {
            console.log ('PAUSED')
            var pauseID = setTimeout(() => {
                
            }, 2147483647);
            document.getElementById("pause").textContent = "Resume";
        } else if (!started && !tryAgain) {
            console.log ('Started')
            started = true
            clearTimeout(startID)
            document.getElementById("pause").textContent = "Pause";
            document.getElementById('finished').className = 'show'
            document.getElementById('lives').className = 'show'
            document.getElementById('verdict').className = 'hide'
        } else {
            console.log ('Resumed')
            clearTimeout(pauseID);
            document.getElementById("pause").textContent = "Pause";
        }
    });
}
