const GAME_STATUS = {
  start: 0,
  playing: 1,
  end: 2
};

const GAME_ACTION = {
  start: 0,
  cont: 1,
  attack: 2,
  heal: 3
};

const DEFAULT_HEALTH = 100;

const getRandomNumber = () => {
  return Math.floor(Math.random() * (10 - 1 + 1)) + 1;
};

export { GAME_STATUS, GAME_ACTION, DEFAULT_HEALTH, getRandomNumber };
