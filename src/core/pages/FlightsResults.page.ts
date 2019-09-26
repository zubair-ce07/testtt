import { ElementArrayFinder } from "protractor";
import { ErrorsDialog, FlightResult, MultiCityForm, TimeSlider, TripSelector } from "../elements";

export interface FlightsResultsPage {
  getTimeSlider(leg: number): TimeSlider;
  
  getTimeSliders(): ElementArrayFinder;
  
  getSearchResult(index: number): FlightResult;
  
  getSearchResults(): ElementArrayFinder;
  
  getMultiCityTripForm(): MultiCityForm;
  
  getTripSelector(): TripSelector;
  
  getErrorDialog(): ErrorsDialog;
}
