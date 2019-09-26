import { MultiCityForm, TripSelector } from "../elements";

export interface FlightsPage {
  clickSearch(): Promise<void>;
  
  getTripSelector(): TripSelector;
  
  getMultiCityTripForm(): MultiCityForm;
}
