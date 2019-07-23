import {commonPage} from "./commonPage";
import {flightResultsPage} from './flightResultsPage'
import {kayakHelper} from "./kayakHelper";

export class kayakFactory {
    public createKayakPageObject = function(type: string) {

        if (type === "commonPage") {
            return new commonPage();
        }
        else if (type === "flightResultsPage") {
            return new flightResultsPage();
        }
        else if (type === "kayakHelper") {
            return new kayakHelper();
        }
    
    }
}