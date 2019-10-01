import { MultiCityForm } from "../elements/forms/multiCityForm";
import { TripSelector } from "../elements/selectors/tripSelector";

export interface FlightsPage {
  getURL(): string;
  
  clickSearch(): Promise<void>;
  
  getTripSelector(): TripSelector;
  
  getMultiCityTripForm(): MultiCityForm;
}
