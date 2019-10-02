import { ElementArrayFinder } from "protractor";
import { ErrorDialog } from "../elements/dialogs/errorDialog";
import { MultiCityForm } from "../elements/forms/multiCityForm";
import { FlightResult } from "../elements/results/flightResult";
import { TripSelector } from "../elements/selectors/tripSelector";
import { TimeSlider } from "../elements/sliders/timeSlider";

export interface FlightsResultsPage {
  getTimeSlider(leg: number): TimeSlider;
  
  getTimeSliders(): ElementArrayFinder;
  
  getSearchResult(index: number): FlightResult;
  
  getSearchResults(): ElementArrayFinder;
  
  getMultiCityTripForm(): MultiCityForm;
  
  getTrip(): TripSelector;
  
  getErrorDialog(): ErrorDialog;
}
