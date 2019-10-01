import { CabinSelector } from "../selectors/cabinSelector";
import { DatePicker } from "../selectors/datePicker";
import { FlightSelector } from "../selectors/flightSelector";

export interface MultiCityForm {
  clearAllLegs(): Promise<void>;
  
  clickSearch(): Promise<void>;
  
  getDatePicker(leg: number): DatePicker;
  
  getCabinSelector(leg: number): CabinSelector;
  
  getOriginSelector(leg: number): FlightSelector;
  
  getDestinationSelector(leg: number): FlightSelector;
  
  getDisplayedLegsCount(): Promise<number>;
  
  isFormVisible(): Promise<boolean>;
  
  makeFormVisible(): Promise<void>;
}
