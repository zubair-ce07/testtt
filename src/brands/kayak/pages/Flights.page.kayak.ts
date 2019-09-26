import { by, element } from "protractor";
import { MultiCityForm, TripSelector } from "../../../core/elements";
import { FlightsPage } from "../../../core/pages";
import { waitUntilInteractive } from "../../../utils/browser.utils";
import { MultiCityFormKayak } from "../elements/forms";
import { TripSelectorKayak } from "../elements/selectors";
import { FlightsResultsPageKayak } from "./FlightsResults.page.kayak";

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
