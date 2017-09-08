import {combineReducers} from "redux";
import {ToggleLoginSignUp} from "./ToggleLoginSignUP";
import {Token} from "./Token";
import {userMems} from "./UserMems";
import {publicMems} from "./PublicMems";
import {userActivities} from "./Activities";
import {signup} from "./User";
import {userCategories} from "./Categories";
import {getMemToUpdate} from "./getMem";
import {reducer as formReducer} from "redux-form";

const allReducers = combineReducers({
    public_mems: publicMems,
    user_activities: userActivities,
    categories: userCategories,
    tab: ToggleLoginSignUp,
    user: signup,
    token: Token,
    user_mems: userMems,
    form: formReducer,
    mem_to_update: getMemToUpdate
});
export default allReducers;
