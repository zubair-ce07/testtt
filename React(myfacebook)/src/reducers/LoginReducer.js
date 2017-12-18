const INITIAL_STATE = {
    news: [],
    selectedNews: []
};

export default function(state=INITIAL_STATE, action)
{
    switch (action.type){
        case "USER_LOGIN":
            return {
                news: [],
                selectedNews: []
            };
        default:
            return state;
    }
}
