import { by, element, ElementArrayFinder } from "protractor";
import { ErrorsDialog, FlightResult, MultiCityForm, TimeSlider, TripSelector } from "../../../core/elements";
import { FlightsResultsPage } from "../../../core/pages";
import { waitUntilInteractive } from "../../../utils/browser.utils";
import { ErrorsDialogKayak } from "../elements/dialogs";
import { FlightResultKayak } from "../elements/FlightResult.kayak";
import { MultiCityFormKayak } from "../elements/forms";
import { TripSelectorKayak } from "../elements/selectors";
import { TimeSliderKayak } from "../elements/sliders";

export class FlightsResultsPageKayak implements FlightsResultsPage {
  static async loadResults() {
    const MINUTE = 60 * 1000;
    
    return waitUntilInteractive(
      element(by.css(`div[aria-label='Flight Search Results'][aria-busy='false']`)),
      MINUTE,
      'Waiting search results list to load completely'
    ).catch(error => console.log(error.message));
  }
  
  getSearchResult(index: number): FlightResult {
    return new FlightResultKayak(
      this.getSearchResults().get(index)
    );
  }
  
  getSearchResults(): ElementArrayFinder {
    return element.all(by.className(`Flights-Results-FlightResultItem`));
  }
  
  getTimeSlider(leg: number): TimeSlider {
    return new TimeSliderKayak(
      element(by.css(`div[id$='-times-takeoff-section-${leg}']`))
    );
  }
  
  getMultiCityTripForm(): MultiCityForm {
    return new MultiCityFormKayak();
  }
  
  getErrorDialog(): ErrorsDialog {
    return new ErrorsDialogKayak();
  }
  
  getTimeSliders(): ElementArrayFinder {
    return element.all(by.className(`timesFilterSection`)).filter(section => section.isDisplayed());
  }
  
  getTripSelector(): TripSelector {
    return new TripSelectorKayak();
  }
  
}
