import { FlightResultDialog } from "../dialogs/flightResultDialog";
import { FlightLeg } from "./flightLeg";

export interface FlightResult {
  getTotalLegs(): Promise<number>;
  
  getFlightLeg(leg: Number): FlightLeg;
  
  getPrice(): Promise<string>;
  
  click(): Promise<void>;
  
  getDialog(): FlightResultDialog;
}
