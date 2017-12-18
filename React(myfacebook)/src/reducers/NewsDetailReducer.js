const INITIAL_STATE = {
    news: [],
    selectedNews: []
};

export default function(state=INITIAL_STATE, action)
{
    switch (action.type){
        case "NEWS_DETAIL":
            return {
                news: [],
                selectedNews: action.payload
            };
        default:
            return state;
    }
}
