const INITIAL_STATE = {
    news: [],
    selectedNews: []
};

export default function(state=INITIAL_STATE, action)
{
    switch (action.type){
        case "NEWS_LIST":
            return {
                news: action.payload,
                selectedNews: []
            };
        default:
            return state;
    }
}
