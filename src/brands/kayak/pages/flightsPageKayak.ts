import { by, element } from "protractor";
import { MultiCityForm } from "../../../core/elements/forms/multiCityForm";
import { TripSelector } from "../../../core/elements/selectors/tripSelector";
import { FlightsPage } from "../../../core/pages/flightsPage";
import { waitUntilInteractive } from "../../../utils/browser.utils";
import { MultiCityFormKayak } from "../elements/forms/multiCityFormKayak";
import { TripSelectorKayak } from "../elements/selectors/tripSelectorKayak";
import { FlightsResultsPageKayak } from "./flightsResultsPageKayak";

export class FlightsPageKayak implements FlightsPage {
  getURL(): string {
    return "https://www.kayak.com/flights";
  }
  
  async loadSearchResults(): Promise<void> {
    const button = element(by.css(`button[id$='-submit-multi']`));
    await waitUntilInteractive(button);
    await button.click();
    await FlightsResultsPageKayak.loadResults();
  }
  
  getMultiCityTripForm(): MultiCityForm {
    return new MultiCityFormKayak();
  }
  
  getTrip(): TripSelector {
    return new TripSelectorKayak();
  }
  
}
