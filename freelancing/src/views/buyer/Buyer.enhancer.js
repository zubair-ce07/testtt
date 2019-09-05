import { compose } from "recompose";
import withAuthorization from "../../hoc/withAuthorization";
import { ROUTES } from "../../constants/routes";

const condition = token => token !== null;
export default compose(withAuthorization(condition, ROUTES.SIGN_IN));
