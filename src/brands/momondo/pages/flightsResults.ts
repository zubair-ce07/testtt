import { by, element, ElementArrayFinder } from "protractor";
import { ErrorDialog } from "../../../core/elements/dialogs/error";
import { MultiCityForm } from "../../../core/elements/forms/multiCity";
import { FlightResult } from "../../../core/elements/results/flight";
import { TripSelector } from "../../../core/elements/selectors/trip";
import { TimeSlider } from "../../../core/elements/sliders/time";
import { FlightsResultsPage } from "../../../core/pages/flightsResults";
import { waitUntilInteractive } from "../../../utils/browser.utils";
import { ErrorDialogMomondo } from "../elements/dialogs/error";
import { MultiCityFormMomondo } from "../elements/forms/multiCity";
import { FlightResultMomondo } from "../elements/results/flight";
import { TripSelectorMomondo } from "../elements/selectors/trip";
import { TimeSliderMomondo } from "../elements/sliders/time";

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
  
  getTripSelector(): TripSelector {
    return new TripSelectorMomondo();
  }
  
}
