import { FlightLeg } from "./flightLeg";

export interface FlightLegDetails extends FlightLeg {
  getCabinClass(): Promise<string>;
  
  getFlightNumber(): Promise<string>;
}
