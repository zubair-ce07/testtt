import { CabinSelector, DateSelector, FlightSelector } from "../selectors";

export interface MultiCityForm {
  clearAll(): Promise<void>;
  
  clickSearch(): Promise<void>;
  
  getDateSelector(leg: number): DateSelector;
  
  getCabinSelector(leg: number): CabinSelector;
  
  getFlightSelector(leg: number): FlightSelector;
  
  getDisplayedLegsCount(): Promise<number>;
  
  isFormVisible(): Promise<boolean>;
  
  makeFormVisible(): Promise<void>;
}
