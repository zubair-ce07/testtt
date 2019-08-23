import { ElementFinder } from "protractor";

interface IFlightSearchPage {
    getAppliedTravelerFilterField(): ElementFinder;

    getMultiCityFormOriginAndDestination(): Promise<{ flightOrigin: string, flightDestination: string }>;

    getMultiCityFormCabinClass(): Promise<string>;

    getMultiCityFormTraveler(): Promise<string>;
}

export default IFlightSearchPage;