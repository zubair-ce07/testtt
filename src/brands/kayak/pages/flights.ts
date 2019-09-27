import { by, element } from "protractor";
import { MultiCityForm } from "../../../core/elements/forms/multiCity";
import { TripSelector } from "../../../core/elements/selectors/trip";
import { FlightsPage } from "../../../core/pages/flights";
import { waitUntilInteractive } from "../../../utils/browser.utils";
import { MultiCityFormKayak } from "../elements/forms/multiCity";
import { TripSelectorKayak } from "../elements/selectors/trip";
import { FlightsResultsPageKayak } from "./flightsResults";

export class FlightsPageKayak implements FlightsPage {
  async clickSearch(): Promise<void> {
    const button = element(by.css(`button[id$='-submit-multi']`));
    await waitUntilInteractive(button);
    await button.click();
    await FlightsResultsPageKayak.loadResults();
  }
  
  getMultiCityTripForm(): MultiCityForm {
    return new MultiCityFormKayak();
  }
  
  getTripSelector(): TripSelector {
    return new TripSelectorKayak();
  }
  
}
