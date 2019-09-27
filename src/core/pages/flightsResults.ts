import { ElementArrayFinder } from "protractor";
import { ErrorDialog } from "../elements/dialogs/error";
import { MultiCityForm } from "../elements/forms/multiCity";
import { FlightResult } from "../elements/results/flight";
import { TripSelector } from "../elements/selectors/trip";
import { TimeSlider } from "../elements/sliders/time";

export interface FlightsResultsPage {
  getTimeSlider(leg: number): TimeSlider;
  
  getTimeSliders(): ElementArrayFinder;
  
  getSearchResult(index: number): FlightResult;
  
  getSearchResults(): ElementArrayFinder;
  
  getMultiCityTripForm(): MultiCityForm;
  
  getTripSelector(): TripSelector;
  
  getErrorDialog(): ErrorDialog;
}
