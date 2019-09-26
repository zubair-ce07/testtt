import { by, element, ElementArrayFinder } from "protractor";
import { ErrorsDialog, FlightResult, MultiCityForm, TimeSlider, TripSelector } from "../../../core/elements";
import { FlightsResultsPage } from "../../../core/pages";
import { waitUntilInteractive } from "../../../utils/browser.utils";
import {
  ErrorDialogMomondo,
  FlightResultMomondo,
  MultiCityFormMomondo,
  TimeSliderMomondo,
  TripSelectorMomondo
} from "../elements";

export class FlightsResultsPageMomondo implements FlightsResultsPage {
  static async loadResults() {
    const MINUTE = 60 * 1000;
    
    return waitUntilInteractive(
      element(by.css(`div[aria-label='Flight Search Results'][aria-busy='false']`)),
      MINUTE,
      'Waiting search results list to load completely'
    ).catch(error => console.log(error.message));
  }
  
  getErrorDialog(): ErrorsDialog {
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
