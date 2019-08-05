import {KayakFlightsPage} from "./KayakFlightsPage";
import {KayakFlightsResultsPage} from './KayakFlightsResultsPage'
import {BookingProviderPage} from "./BookingProviderPage";

export class KayakFactory {
    public createKayakPageObject = function(type: string) {

        if (type === "KayakFlightsPage") {
            return new KayakFlightsPage();
        }
        else if (type === "flightKayakFlightsResultsPageResultsPage") {
            return new KayakFlightsResultsPage();
        }
        else if (type === "BookingProviderPage") {
            return new BookingProviderPage();
        }
    }
}