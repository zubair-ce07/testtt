import { FlightResultDialog } from "../dialogs/flightResultDialog";
import { FlightLegDetails } from "./flightLegDetails";

export interface FlightResult {
  getTotalLegs(): Promise<number>;
  
  getFlightLeg(leg: Number): FlightLegDetails;
  
  getPrice(): Promise<string>;
  
  click(): Promise<void>;
  
  getDialog(): FlightResultDialog;
}
