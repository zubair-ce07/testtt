import { by, element, ElementArrayFinder } from "protractor";
import { ErrorDialog } from "../../../core/elements/dialogs/errorDialog";
import { MultiCityForm } from "../../../core/elements/forms/multiCityForm";
import { FlightResult } from "../../../core/elements/results/flightResult";
import { TripSelector } from "../../../core/elements/selectors/tripSelector";
import { TimeSlider } from "../../../core/elements/sliders/timeSlider";
import { FlightsResultsPage } from "../../../core/pages/flightsResultsPage";
import { waitUntilInteractive } from "../../../utils/browser.utils";
import { ErrorDialogKayak } from "../elements/dialogs/errorDialogKayak";
import { MultiCityFormKayak } from "../elements/forms/multiCityFormKayak";
import { FlightResultKayak } from "../elements/results/flightResultKayak";
import { TripSelectorKayak } from "../elements/selectors/tripSelectorKayak";
import { TimeSliderKayak } from "../elements/sliders/timeSliderKayak";

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
  
  getErrorDialog(): ErrorDialog {
    return new ErrorDialogKayak();
  }
  
  getTimeSliders(): ElementArrayFinder {
    return element.all(by.className(`timesFilterSection`)).filter(section => section.isDisplayed());
  }
  
  getTripSelector(): TripSelector {
    return new TripSelectorKayak();
  }
  
}
