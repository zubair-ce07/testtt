import {SEARCH_ACTION} from '../constants';

const weatherData = function(state=[], action){
   if (action.type === SEARCH_ACTION) {
        const n = [
            action.payload,
            ...state
        ];
        console.log(n);
        return n;
    }
    return state;
};
export default weatherData;