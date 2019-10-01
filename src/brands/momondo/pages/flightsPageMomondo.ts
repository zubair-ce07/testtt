import { by, element } from "protractor";
import { MultiCityForm } from "../../../core/elements/forms/multiCityForm";
import { TripSelector } from "../../../core/elements/selectors/tripSelector";
import { FlightsPage } from "../../../core/pages/flightsPage";
import { MultiCityFormMomondo } from "../elements/forms/multiCityFormMomondo";
import { TripSelectorMomondo } from "../elements/selectors/tripSelectorMomondo";
import { FlightsResultsPageMomondo } from "./flightsResultsPageMomondo";

export class FlightsPageMomondo implements FlightsPage {
  getURL(): string {
    return "https://global.momondo.com";
  }
  
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
