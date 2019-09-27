import { by, element } from "protractor";
import { MultiCityForm } from "../../../core/elements/forms/multiCity";
import { TripSelector } from "../../../core/elements/selectors/trip";
import { FlightsPage } from "../../../core/pages/flights";
import { MultiCityFormMomondo } from "../elements/forms/multiCity";
import { TripSelectorMomondo } from "../elements/selectors/trip";
import { FlightsResultsPageMomondo } from "./flightsResults";

export class FlightsPageMomondo implements FlightsPage {
  async clickSearch(): Promise<void> {
    element(by.css(`button[id$='-submit-multi']`)).click();
    await FlightsResultsPageMomondo.loadResults();
  }
  
  getMultiCityTripForm(): MultiCityForm {
    return new MultiCityFormMomondo();
  }
  
  getTripSelector(): TripSelector {
    return new TripSelectorMomondo();
  }
  
}
