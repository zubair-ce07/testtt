import { ElementFinder } from "protractor";

interface IFlightSearchPage {
    getAppliedTravelerFilterField(): ElementFinder;

    getMultiCityFormOriginAndDestination(): Promise<{ flightOrigin: string, flightDestination: string }>;

    getMultiCityFormCabinClass(): Promise<string>;

    getMultiCityFormTraveler(): Promise<string>;

    getMultiCityFormDate(): Promise<string>;

    getSearchedFlightTakeOffTime(flightResultNo: number): Promise<string>;

    getSearchedFlightsCount(): Promise<number>;
}

export default IFlightSearchPage;