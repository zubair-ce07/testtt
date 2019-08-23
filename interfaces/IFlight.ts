import { ElementFinder } from "protractor";

interface IFlight {
    selectFlightTypeMultiCity(): Promise<void>;

    setLegNo(legNo: number): void;

    getLegNo(): number;

    getOriginField(): Promise<ElementFinder>;

    getDestinationField(): Promise<ElementFinder>;

    selectFirstOptionFromOriginsDropdown(): Promise<void>;

    selectFirstOptionFromDestinationDropdown(): Promise<void>;

    setFlightDepartureDate(): Promise<string>;

    setFlightTypeToBusiness(): Promise<void>;

    getSelectedTravelerText(): Promise<string>;

    isFlightsSearchPageDisplayed(): Promise<boolean>;
}

export default IFlight;