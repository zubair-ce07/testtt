import {KayakFlightsPage} from "./KayakFlightsPage";
import {KayakFlightsResultsPage} from './KayakFlightsResultsPage'
import { MomondoFlightsPage } from "./MomondoFlightsPage";
import { MomondoFlightsResultsPage } from "./MomondoFlightsResultPage";

export class Factory {
    public createPageObject(type: string): any {

        if (type === "KayakFlightsPage") {
            return new KayakFlightsPage();
        }
        else if (type === "KayakFlightsResultsPage") {
            return new KayakFlightsResultsPage();
        }
        else if (type === "MomondoFlightsPage") {
            return new MomondoFlightsPage();
        }
        else if(type === "MomondoFlightsResultsPage") {
            return new MomondoFlightsResultsPage();
        }
    }
}