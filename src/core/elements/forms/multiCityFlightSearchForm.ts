import { FlightForm } from "./flightForm";

export interface MultiCityFlightSearchForm {
  getFlightLeg(leg: number): FlightForm;
  
  getFlightLegs(): Promise<FlightForm[]>;
  
  addFlightLegs(count: number): Promise<unknown>;
  
  removeFlightLegs(count: number): Promise<unknown>;
}
