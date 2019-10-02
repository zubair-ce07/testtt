import { MultiCityForm } from "../elements/forms/multiCityForm";
import { TripSelector } from "../elements/selectors/tripSelector";

export interface FlightsPage {
  getURL(): string;
  
  loadSearchResults(): Promise<void>;
  
  getTrip(): TripSelector;
  
  getMultiCityTripForm(): MultiCityForm;
}
