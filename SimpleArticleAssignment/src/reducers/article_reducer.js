export default function (state=[], action) {

    switch (action.type) {
        case "ARTICLE_LIST":
            debugger;
            return action.payload.data;
    }
    return state;
}