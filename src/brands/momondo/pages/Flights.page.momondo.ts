import { by, element } from "protractor";
import { MultiCityForm, TripSelector } from "../../../core/elements";
import { FlightsPage } from "../../../core/pages";
import { MultiCityFormMomondo } from "../elements/forms";
import { TripSelectorMomondo } from "../elements/selectors";
import { FlightsResultsPageMomondo } from "./FlightsResults.page.momondo";

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
