import { FlightLegDetails } from "../results/flightLegDetails";

export interface FlightResultDialog {
  getTotalLegs(): Promise<number>;
  
  getFlightLeg(leg: number): FlightLegDetails;
  
  getTravellers(): Promise<string>;
  
  getReturnDate(): Promise<string>;
  
  getDepartureDate(): Promise<string>;
  
  getPrice(): Promise<string>;
  
  isDisplayed(): Promise<boolean>;
  
  close(): Promise<void>;
}
