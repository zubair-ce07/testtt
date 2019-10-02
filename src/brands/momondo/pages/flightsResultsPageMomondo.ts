import { by, element, ElementArrayFinder } from "protractor";
import { ErrorDialog } from "../../../core/elements/dialogs/errorDialog";
import { MultiCityForm } from "../../../core/elements/forms/multiCityForm";
import { FlightResult } from "../../../core/elements/results/flightResult";
import { TripSelector } from "../../../core/elements/selectors/tripSelector";
import { TimeSlider } from "../../../core/elements/sliders/timeSlider";
import { FlightsResultsPage } from "../../../core/pages/flightsResultsPage";
import { waitUntilInteractive } from "../../../utils/browser.utils";
import { ErrorDialogMomondo } from "../elements/dialogs/errorDialogMomondo";
import { MultiCityFormMomondo } from "../elements/forms/multiCityFormMomondo";
import { FlightResultMomondo } from "../elements/results/flightResultMomondo";
import { TripSelectorMomondo } from "../elements/selectors/tripSelectorMomondo";
import { TimeSliderMomondo } from "../elements/sliders/timeSliderMomondo";

export class FlightsResultsPageMomondo implements FlightsResultsPage {
  static async loadResults() {
    const MINUTE = 60 * 1000;
    
    return waitUntilInteractive(
      element(by.css(`div[aria-label='Flight Search Results'][aria-busy='false']`)),
      MINUTE,
      'Waiting search results list to load completely'
    ).catch(error => console.log(error.message));
  }
  
  getErrorDialog(): ErrorDialog {
    return new ErrorDialogMomondo();
  }
  
  getMultiCityTripForm(): MultiCityForm {
    return new MultiCityFormMomondo();
  }
  
  getSearchResult(index: number): FlightResult {
    return new FlightResultMomondo(
      this.getSearchResults().get(index)
    );
  }
  
  getSearchResults(): ElementArrayFinder {
    return element.all(by.className(`Flights-Results-FlightResultItem`));
  }
  
  getTimeSlider(leg: number): TimeSlider {
    return new TimeSliderMomondo(leg);
  }
  
  getTimeSliders(): ElementArrayFinder {
    return element.all(by.className(`timesFilterSection`)).filter(element => element.isDisplayed());
  }
  
  getTrip(): TripSelector {
    return new TripSelectorMomondo();
  }
  
}
